var app = angular.module('myApp', ['ui.router']);

app.config(function($stateProvider, $urlRouterProvider, $locationProvider) {
  $urlRouterProvider.otherwise('/');
  $stateProvider
    .state('home', {
      url: '/',
      templateUrl: 'templates/homepage.html',
      controller: 'PostCtrl'
    })
    .state('login', {
      url: '/login/',
      templateUrl: 'templates/login.html',
      controller: 'AuthCtrl'
    })
    .state('logout', {
      url: '/logout/',
      template: '<div ng-controller="AuthCtrl" data-ng-init="logout()"></div>',
      controller: 'AuthCtrl'
    })
    .state('admin_users_create', {
      url: '/admin/users/create/',
      templateUrl: 'templates/admin_users_create.html',
      controller: 'AdminUsersCreateCtrl'
    })
    .state('admin_users', {
      url: '/admin/users/',
      templateUrl: 'templates/admin_users.html',
      controller: 'AdminUsersCtrl'
    })
    .state('admin_users_update', {
      url: '/admin/users/:id/',
      templateUrl: 'templates/admin_users_update.html',
      controller: 'AdminUsersUpdateCtrl'
    })
    .state('user_settings', {
      url: '/user/settings/',
      templateUrl: 'templates/user_settings.html',
      controller: 'UserSettingsCtrl'
    })
    .state('submit_post', {
      url: '/posts/add/',
      templateUrl: 'templates/submit_post.html',
      controller: 'SubmitPostCtrl'
    })
    .state('single_post', {
      url: '/posts/:id/',
      templateUrl: 'templates/single_post.html',
      controller: 'SinglePostCtrl'
    })
    .state('update_post', {
      url: '/posts/:id/edit/',
      templateUrl: 'templates/update_post.html',
      controller: 'UpdatePostCtrl'
    });
});

app.config(function($httpProvider, $windowProvider) {
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

  var API_URL = 'http://127.0.0.1:8000/';

  function apiInterceptor($q) {
    return {
      request: function (config) {
        var url = config.url;
        // ignore template requests
        if (url.substr(url.length - 5) == '.html') {
          return config || $q.when(config);
        }
        config.url = API_URL + config.url;
          return config || $q.when(config);
      }
    }
  }
  $httpProvider.interceptors.push(apiInterceptor);

  var $window = $windowProvider.$get();
  $httpProvider.defaults.headers.common['Authorization'] = "Token " + $window.localStorage.getItem('token');
});

app.config(function ($interpolateProvider) {
  $interpolateProvider.startSymbol('[[').endSymbol(']]');
});

app.run(function ($rootScope, $state, $http, $window) {
  $rootScope.$on('$stateChangeSuccess', function() {
      if ($state.current.name == 'home')
        jQuery('html, body').animate({ scrollTop: 0 }, 200);
  });

  if ($window.localStorage.getItem('token') != null) {
    $http.get('api/members/profile/').then(
      function(response) {
        $window.localStorage.setItem('id', response.data.id);
        $window.localStorage.setItem('username', response.data.username);
        $window.localStorage.setItem('is_admin', response.data.is_admin);
        $window.localStorage.setItem('is_author', response.data.is_author);
        $window.localStorage.setItem('date_joined', response.data.date_joined);
        $window.localStorage.setItem('email', response.data.email);
        $window.localStorage.setItem('fullname', response.data.fullname);
        $window.localStorage.setItem('last_login', response.data.last_login);
      },
      function(response) {
        // in case of token expires
        if ((response.status == 401) || (response.status == 500))
          $state.go('logout');
      }
    );
  }
});

app.factory('range', function () {
  return {
    getRange: function(start, stop, step) {
      if (typeof stop == 'undefined') {
          // one param defined
          stop = start;
          start = 0;
      }
      if (typeof step == 'undefined') {
          step = 1;
      }
      if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
          return [];
      }
      var result = [];
      for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
          result.push(i);
      }
      return result;
    }
  }
});