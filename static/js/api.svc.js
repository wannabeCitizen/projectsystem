/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var factory = {};

    factory.OrgApi = ['$resource', function ($resource) {
        return $resource('/api/org/:orgId', {orgId: '@unique'}, {
            update: { method: 'PUT' },
            addOwner: { method: 'PUT', url: '/api/org/:orgId/owner'},
            delOwner: { method: 'DELETE', url: '/api/org/:orgId/owner/:userId'},
            addMember: { method: 'PUT', url: '/api/org/:orgId/member'},
            delMember: { method: 'DELETE', url: '/api/org/:orgId/member/:userId'}
        });
    }];

    factory.IdeaApi = ['$resource', function ($resource) {
        return $resource('/api/org/:orgId/idea/:ideaId', {orgId: '@orgId', ideaId: '@unique'}, {
            update: { method: 'PUT' }
        });
    }];

    return factory;
});
