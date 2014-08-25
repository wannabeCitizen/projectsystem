/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var dir = {};

    dir.userSelector = ['UserApi', function (UserApi) {
        return {
            restrict: 'E',
            templateUrl: 'static/template/dir/userSelector.html',
            scope: {
                user: '='
            },
            link: function (scope) {
                scope.search = function (str) {
                    return UserApi.search({ search: str }).$promise;
                };
            }
        };
    }];

    return dir;
});
