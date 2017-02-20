app.controller('AdminUsersCreateCtrl', function($rootScope, $location, $scope, $http, $window, $state) {
	$rootScope.hide = false;
	$rootScope.header = 'Admin | Create User';
	$scope.login = $window.localStorage.getItem('login');
	$scope.admin = JSON.parse($window.localStorage.getItem('is_admin'));
	$scope.user = {};

	$scope.create = function() {
		$http.post('api/members/', $scope.user).then(
			function(response) {
				$scope.user = response.data;
				url = 'admin/users/';
				$location.path(url);
				$state.go('admin_users');
			},
			function(response) {
				alert('User cannot be created.');
				$state.reload();
			}
		);
	}
});

app.controller('AdminUsersCtrl', function($rootScope, $scope, $http, $window) {
	$rootScope.hide = false;
	$rootScope.header = 'Admin | Update Users';
	$scope.login = $window.localStorage.getItem('login');
	$scope.admin = JSON.parse($window.localStorage.getItem('is_admin'));

	$scope.init = function() {
		$http.get('api/members/').then(
			function(response) {
				console.log(response.data)
				$scope.members = response.data;
			}
		);
	}
});

app.controller('AdminUsersUpdateCtrl', function($rootScope, $stateParams, $scope, $http, $window, $state) {
	$rootScope.hide = false;
	$scope.login = $window.localStorage.getItem('login');
	$scope.username = $window.localStorage.getItem('username');
	$scope.admin = JSON.parse($window.localStorage.getItem('is_admin'));
	$scope.user = {};

	$scope.init = function() {
		$http.get('api/members/' + $stateParams.id +'/').then(
			function(response) {
				$scope.user = response.data;
				$rootScope.header = "Blog | Update " + $scope.user.username;
			},
			function(response) {
				alert('That user does not exist!');
				$state.go('admin_users');
			}
		);
	}

	$scope.update = function() {
		$http.put('api/members/' + $stateParams.id +'/', $scope.user).then(
			function(response) {
				alert('User has been updated!');
				if ($scope.username == $scope.user.username) {
					if (($scope.user.password != null) && ($scope.user.password != ""))
						$state.go('logout');
					else
						$window.location.reload();
				}
				else
					$window.location.reload();
			},
			function(response) {
				alert('User cannot be updated!');
			}
		);
	}

	$scope.deactivate = function() {
		$http.delete('api/members/' + $stateParams.id +'/').then(
			function(response) {
				alert('User has been deactivate!');
				if ($scope.username == $scope.user.username)
					$state.go('logout');
				else
					$window.location.reload();
			}
		);
	}

	$scope.activate = function() {
		$scope.user.is_active = true;
		$http.put('api/members/' + $stateParams.id +'/', $scope.user).then(
			function(response) {
				alert('User has been activate!');
				$window.location.reload();
			}
		);
	}
});