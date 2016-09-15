var app = angular.module('vilde');

app.service('AppendCredentialsService', [function() {
    var self = this;

    self.appendCredentials = function(object, username, token) {
        object['username'] = username;
        object['token'] = token;
    }
}]);