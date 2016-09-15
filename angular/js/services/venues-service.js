var app = angular.module('coreModule');

app.factory('VenuesService', ['$http', '$rootScope', function($http, $rootScope) {

    var venuesEndpoint = $rootScope.serverRoot + 'venue';
    var promise;

    var venuesService = {
        getVenues: function() {
            if(!promise) {
                promise = $http.get(venuesEndpoint).then(function(response) {
                    return response.data
                });
            } return promise;
        },
		refreshVenues: function() {
            promise = $http.get(venuesEndpoint).then(function(response) {
                return response.data
            });
            return promise;
        }
    };
    return venuesService;

}]);