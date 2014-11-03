/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var factory = {};

    factory.UserApi = ['$resource', function ($resource) {
        return $resource('/api/user/:userId', {userId: '@unique'}, {
            search: { method: 'GET', isArray: true },
            getList: { method: 'POST', url: '/api/user/list', isArray: true }
        });
    }];

    return factory;
});
