/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var factory = {};

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
