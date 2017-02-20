app.controller('UserSettingsCtrl', function($rootScope, $http, $scope, $filter, $window, $state) {
	$rootScope.hide = false;
	$scope.date_joined = $window.localStorage.getItem('date_joined');
	$scope.email = $window.localStorage.getItem('email');
    $scope.fullname = $window.localStorage.getItem('fullname');
    $scope.last_login = $window.localStorage.getItem('last_login');
    $scope.username = $window.localStorage.getItem('username');
    $scope.login = $window.localStorage.getItem('login');
    $scope.password = {};

	$rootScope.header = 'Blog | Settings';

	$scope.init = function() {
		$scope.date_joined = $filter('date')($scope.date_joined, 'yyyy-MM-dd');
	}

	$scope.reset = function() {
		$http.post('api/members/profile/reset_password/', $scope.password).then(
			function(response) {
				alert('Password has been successfully updated!');
				$state.go('logout');
			},
			function(response) {
				alert('Please check your password again!');
			}
		);
	}
});