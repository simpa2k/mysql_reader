var app = angular.module('vilde');

app.service('SendObjectService', ['$http', function($http) {
    var self = this;

    function countNumberOfProperties(object) {
        var counter = 0;

        angular.forEach(object, function() {
            counter++;
        });

        return counter;
    }

    function constructUriFromObject(object) {
        var uri = '';
        var numberOfIterations = countNumberOfProperties(object);
        var counter = 0;

        angular.forEach(object, function(value, key) {
            var encodedValue = encodeURIComponent(value);
            uri += key + '=' + encodedValue;
            counter++;
            if(counter < numberOfIterations) {
                uri += '&';
            }
        });
        return uri;
    };

    self.appendToUri = function(uri, object) {
        return uri + '&' + constructUriFromObject(object);
    };

    self.createUri = function(endpoint, object) {
        var uri = endpoint + '?';
        return uri + constructUriFromObject(object);
    };

    self.putObject = function(endpoint, object, callback) {
        $http.put(self.createUri(endpoint, object)).then(function(response) {
            callback(response.data);
        });
    };

    self.postObject = function(endpoint, object, callback) {
        $http.post(self.createUri(endpoint, object)).then(function(response) {
            callback(response.data);
        });
    };

    self.deleteObject = function(endpoint, object, callback) {
        $http.delete(self.createUri(endpoint, object)).then(function(response) {
            callback(response.data);
        });
    };
}]);