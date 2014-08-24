/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var factory = {};

    factory.OrgApi = ['$resource', function ($resource) {
        return $resource('/api/org/:orgId', {orgId: '@unique'});
    }];

    return factory;
});
