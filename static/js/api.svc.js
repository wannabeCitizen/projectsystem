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

    factory.OrgApi = ['$resource', function ($resource) {
        return $resource('/api/org/:orgId', {orgId: '@unique'}, {
            update: { method: 'PUT' },
            addOwner: { method: 'PUT', url: '/api/org/:orgId/owner'},
            delOwner: { method: 'DELETE', url: '/api/org/:orgId/owner/:userId'},
            addMember: { method: 'PUT', url: '/api/org/:orgId/member'},
            delMember: { method: 'DELETE', url: '/api/org/:orgId/member/:userId'}
        });
    }];

    factory.ProjectApi = ['$resource', function ($resource) {
        return $resource('/api/org/:orgId/project/:projectId', {orgId: '@orgId', projectId: '@unique'}, {
            update: { method: 'PUT'},
            addMember: { method: 'PUT', url: '/api/org/:orgId/project/:projectId/member/:userId'},
            delMember: { method: 'DELETE', url: '/api/org/:orgId/project/:projectId/member/:userId'},
            follower: { method: 'PUT', url: '/api/org/:orgId/project/:projectId/follow'},
            unfollower: { method: 'DELETE', url: '/api/org/:orgId/project/:projectId/follow'},
            addRole: { method: 'POST', url: '/api/org/:orgId/project/:projectId/role'},
            delRole: { method: 'DELETE', url: '/api/org/:orgId/project/:projectId/role'},
            updateRole: { method: 'PUT', url: '/api/org/:orgId/project/:projectId/role'},
            addTask: { method: 'POST', url: '/api/org/:orgId/project/:projectId/task'},
            delTask: { method: 'DELETE', url: '/api/org/:orgId/project/:projectId/task'},
            updateTask: { method: 'PUT', url: '/api/org/:orgId/project/:projectId/task'},
            addVote: { method: 'POST', url: '/api/org/:orgId/project/:projectId/vote'},
            delVote: { method: 'DELETE', url: '/api/org/:orgId/project/:projectId/vote'},
            updateVote: { method: 'PUT', url: '/api/org/:orgId/project/:projectId/vote'},
            castBallot: { method: 'PUT', url: '/api/org/:orgId/project/:projectId/ballot'},
            addPhase: { method: 'POST', url: '/api/org/:orgId/project/:projectId/phase'},
            delPhase: { method: 'DELETE', url: '/api/org/:orgId/project/:projectId/phase'},
            updatePhase: { method: 'PUT', url: '/api/org/:orgId/project/:projectId/phase'},
            addComment: { method: 'POST', url: '/api/org/:orgId/project/:projectId/comment'},
            delComment: { method: 'DELETE', url: '/api/org/:orgId/project/:projectId/comment'},
            updateComment: { method: 'PUT', url: '/api/org/:orgId/project/:projectId/comment'},
            addReply: { method: 'POST', url: '/api/org/:orgId/project/:projectId/comment/:commentId/reply'},
            delReply: { method: 'DELETE', url: '/api/org/:orgId/project/:projectId/comment/:commentId/reply'},
            updateReply: { method: 'PUT', url: '/api/org/:orgId/project/:projectId/comment/:commentId/reply'}
        });
    }];

    return factory;
});
