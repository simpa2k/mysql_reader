var app = angular.module('coreModule');

app.factory('MembersService', ['$http', '$rootScope', function($http, $rootScope) {

    var membersEndpoint = $rootScope.serverRoot + 'member';
    var promise;

    var membersService = {
        getMembers: function() {
            if(!promise) {
                promise = $http.get(membersEndpoint).then(function(response) {
                    return response.data
                });
            } return promise;
        },
		refreshMembers: function() {
            promise = $http.get(membersEndpoint).then(function(response) {
                return response.data
            });
            return promise;
        }
    };
    return membersService;

}]);