var app = angular.module('coreModule');

app.factory('GigsService', ['$http', '$rootScope', function($http, $rootScope) {

    var gigsEndpoint = $rootScope.serverRoot + 'gig';
    var promise;

    var gigsService = {
        getGigs: function() {
            if(!promise) {
                promise = $http.get(gigsEndpoint).then(function(response) {
                    return response.data
                });
            } return promise;
        },
		refreshGigs: function() {
            promise = $http.get(gigsEndpoint).then(function(response) {
                return response.data
            });
            return promise;
        }
    };
    return gigsService;

}]);