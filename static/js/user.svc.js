/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var factory = {};

    factory.UserApi = ['$resource', function ($resource) {
        return $resource('/api/user', {userId: '@unique'}, {
            search: { method: 'GET', isArray: true }
        });
    }];

    factory.UserSvc = ['$rootScope', function ($rootScope) {
        var svc = {};

        svc.usersEqual = function (u1, u2) {
            return u1 && u2 && (u1.google_id === u2.google_id);
        };

        svc.isCurrentUser = function (u) {
            return svc.usersEqual(u, $rootScope.currentUser);
        };

        return svc;
    }];

    return factory;
});
