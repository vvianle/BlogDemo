app.controller('SubmitPostCtrl', function($rootScope, $state, $scope, $http, $window) {
	$rootScope.header = 'Blog | Add Post';
	$rootScope.hide = false;
	$scope.login = $window.localStorage.getItem('login');
	$scope.admin = JSON.parse($window.localStorage.getItem('is_admin'));
	$scope.author = JSON.parse($window.localStorage.getItem('is_author'));
	$scope.post = {}
	$scope.create = function() {
		$http.post('api/posts/add/', $scope.post).then(
			function(response) {
				$scope.post = response.data;
				$state.go('home');
			},
			function(response) {
				alert('Post cannot be added.');
				$state.reload();
			}
		);
	}
});

app.controller('UpdatePostCtrl', function($rootScope, $stateParams, $state, $scope, $http, $window) {
	$rootScope.header = 'Blog | Update Post';
	$rootScope.hide = false;
	$scope.login = $window.localStorage.getItem('login');
	$scope.admin = JSON.parse($window.localStorage.getItem('is_admin'));
	$scope.author = JSON.parse($window.localStorage.getItem('is_author'));
	$scope.username = $window.localStorage.getItem('username');
	$scope.post = {};

	$scope.init = function() {
		$http.get('api/posts/' + $stateParams.id + '/').then(
			function(response) {
				$scope.post = response.data;
				$scope.owner = ($scope.post.author.username == $scope.username);
			},
			function(response) {
				alert('Post does not exist.');
				$state.go('home');
			}
		);
	}

	$scope.update = function() {
		$http.put('api/posts/' + $stateParams.id + '/edit/', $scope.post).then(
			function(response) {
				alert("Post has been updated!");
				$state.go('single_post', {id: $stateParams.id});
			},
			function(response) {
				alert('Post cannot be updated.');
				console.log(response.data);
			}
		);
	}
});

app.controller('PostCtrl', function($rootScope, $scope, $http, $window){
  	$rootScope.header = 'Welcome | Blog';
  	$rootScope.hide = false;
  	$scope.posts = {};
  	$scope.numCmt = [];
  	$scope.username = $window.localStorage.getItem('username');

  	$scope.init = function() {
		$http.get('api/posts/').then(
			function(response) {
				$scope.posts = response.data;
				for (x = 1; x <= $scope.posts.length; x++) {
					$http.get('api/posts/' + x +'/comments/').then(
						function(response) {
							$scope.numCmt.push(response.data.length);
						}
					);
				}
			}
		);	
	}

	$scope.getNumComment = function(index) {
		return $scope.numCmt[index];
	}

	$scope.convertTimestamp = function(time) {
		var date = new Date(time).toUTCString();
		return date.slice(0, date.length-3);
	}
});

app.controller('SinglePostCtrl', function($rootScope, $stateParams, $scope, $http, $window){
  	$rootScope.hide = false;
  	$scope.login = $window.localStorage.getItem('login');
  	$scope.username = $window.localStorage.getItem('username');
  	$scope.post = {};
  	$scope.comments = {};
  	$scope.cmt = {};

  	$scope.init = function() {
		$http.get('api/posts/' + $stateParams.id + '/').then(
			function(response) {
				$scope.post = response.data;
				$rootScope.header = 'Blog | ' + $scope.post.title;
			},
			function(response) {
				$rootScope.header = 'Blog';
				alert('Post does not exist.');
				$state.go('home');
			}
		);

		$http.get('api/posts/' + $stateParams.id + '/comments/').then(
			function(response) {
				$scope.comments = response.data;
			}
		);
	}

	$scope.comment = function() {
		$http.post('api/posts/' + $stateParams.id + '/comments/add/', $scope.cmt).then(
			function(response) {
				$window.location.reload();
			},
			function(response) {
				alert('Cannot add comment.');
			}
		);
	}

	$scope.convertTimestamp = function(time) {
		var date = new Date(time).toUTCString();
		return date.slice(0, date.length-3);
	}
});