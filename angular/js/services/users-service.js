var app = angular.module('coreModule');

app.factory('UsersService', ['$http', '$rootScope', function($http, $rootScope) {

    var usersEndpoint = $rootScope.serverRoot + 'user';
    var promise;

    var usersService = {
        getUsers: function() {
            if(!promise) {
                promise = $http.get(usersEndpoint).then(function(response) {
                    return response.data
                });
            } return promise;
        },
		refreshUsers: function() {
            promise = $http.get(usersEndpoint).then(function(response) {
                return response.data
            });
            return promise;
        }
    };
    return usersService;

}]);