var app = angular.module('coreModule');

app.factory('ContactpersonsService', ['$http', '$rootScope', function($http, $rootScope) {

    var contactpersonsEndpoint = $rootScope.serverRoot + 'contactperson';
    var promise;

    var contactpersonsService = {
        getContactpersons: function() {
            if(!promise) {
                promise = $http.get(contactpersonsEndpoint).then(function(response) {
                    return response.data
                });
            } return promise;
        },
		refreshContactpersons: function() {
            promise = $http.get(contactpersonsEndpoint).then(function(response) {
                return response.data
            });
            return promise;
        }
    };
    return contactpersonsService;

}]);