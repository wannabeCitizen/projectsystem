/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var factory = {};

    factory.UserApi = ['$resource', function ($resource) {
        return $resource('/api/user', {userId: '@unique'}, {
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

    factory.IdeaApi = ['$resource', function ($resource) {
        return $resource('/api/org/:orgId/idea/:ideaId', {orgId: '@my_org.unique', ideaId: '@unique'}, {
            update: { method: 'PUT' },
            follow: { method: 'PUT', url: '/api/org/:orgId/idea/:ideaId/follow'},
            unfollow: { method: 'DELETE', url: '/api/org/:orgId/idea/:ideaId/follow'}
        });
    }];

    factory.ProjectApi = ['$resource', function ($resource) {
        return $resource('/api/org/:orgId/project/:projectId', {orgId: '@orgId', projectId: '@unique'}, {
            update: { method: 'PUT'},
            addMember: { method: 'PUT', },
            delMember: { method: 'DELETE', },
            addFollower: { method: 'PUT',},
            delFollower: { method: 'DELETE',},
            addRole: { method: 'POST', },
            delRole: { method: 'DELETE',},
            updateRole: { method: 'PUT',},
            addTask: { method: 'POST',},
            delTask: { method: 'DELETE',},
            updateTask: { method: 'PUT',},
            addVote: { method: 'POST',},
            delVote: { method: 'DELETE',},
            updateRole: { method: 'PUT',},
            castBallot: { method: 'PUT', },
            addPhase: { method: 'POST',},
            delPhase: { method: 'DELETE',},
            updatePhase: { method: 'PUT',},
            addComment: { method: 'POST',},
            delComment: { method: 'DELETE',},
            updateComment: { method: 'PUT',},
            addReply: { method: 'POST',},
            delReply: { method: 'DELETE',},
            updateReply: { method: 'PUT',},
        });
    }];

    return factory;
});
