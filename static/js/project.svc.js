/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore', 'moment'], function (angular, _, moment) {
    'use strict';

    var factory = {};
    // factory.Vote = ['$http', 'UserSvc', function ($http, UserSvc) {  
    //     var Vote = function (resource, project) {
    //         angular.extend(this, resource);
    //     };
    // }];



    factory.Project = ['$http', '$resource', 'UserSvc', function ($http, $resource, UserSvc, Version) {
        var Project = function (resource) {
            angular.extend(this, resource);
            this.orgId = this.my_org && this.my_org.unique;
            this.projectId = this.unique;
            this.url = '/api/org' + this.orgId + '/project/' + this.projectId;

            // _(this.comments).each(function () {

            // });

            // _(this.votes).each(function () {

            // });

            this.serialize = function () {
                return _(this).pick('title', 'unique', 'short_description', 'based_on', 'budget', 'quorum', 'majority', 'text', 'complete');
            };

            this.save = function () {
                return $http.put(this.url, this.serialize())
                    .then(angular.bind(this, function (response) {
                        angular.extend(this, response.data);
                        return this;
                    }));
            };

            this.userIsMember = function (memList) {
                return _(memList).find(function (m) { return UserSvc.isCurrent(m); });
            };

            this.userIsFollowing = function () {
                return _(this.followers).find(function (follower) {
                    return UserSvc.isCurrentUserId(follower);
                });
            };

            this.follow = function () {
                return this.$follow().then(angular.bind(this, function () {
                    this.followers.push(UserSvc.currentUser.id);
                    return this;
                }));
            };

            this.unfollow = function () {
                return this.$unfollow().then(angular.bind(this, function () {
                    this.followers = _(this.followers).without(UserSvc.currentUser.id);
                    return this;
                }));
            };

            this.addRole = function (newRole) {
                return Project.api.addRole(_(this).pick('orgId', 'projectId'), newRole).$promise.then(angular.bind(this, function (r) {
                    this.roles.push(r);
                    return r;
                }));
            };

            this.updateRole = function (role) {
                return this.$updateRole(_(this).pick('orgId', 'projectId'), role).$promise.then(angular.bind(this, function () {
                    var existing = _(this.roles).find(function (me) { return me.index === role.index; });
                    if (existing) {
                        angular.copy(role, existing);
                    }
                    return existing;
                }));

            };

            this.delRole = function (oldRole) {
                return this.$delRole(_(this).pick('orgId', 'projectId'), oldRole).$promise.then(angular.bind(this, function () {
                    this.roles = _(this.roles).without(oldRole);
                }));

            };

            this.addTask = function (newTask) {
                return this.$addTask(_(this).pick('orgId', 'projectId'), newTask).$promise.then(angular.bind(this, function (t) {
                    this.tasks.push(t);
                    return t;
                }));

            };

            this.updateTask = function (task) {
                return this.$updateTask(_(this).pick('orgId', 'projectId'), task).$promise.then(angular.bind(this, function () {
                    var existing = _(this).find(function (t) { return t.index === task.index; });
                    if (existing) {
                        angular.copy(task, existing);
                    }
                    return existing;
                }));

            };

            this.delTask = function (oldTask) {
                return this.$delTask(_(this).pick('orgId', 'projectId'), oldTask).$promise.then(angular.bind(this, function () {
                    this.tasks = _(this.tasks).without(oldTask);
                }));

            };

            this.addMember = function (user) {
                return this.$addMember(_(this).pick('orgId', 'projectId'), user).$promise.then(function () {
                    this.members.push(user);
                });

            };

            this.delMember = function (user) {
                return this.$delMember(_(this).pick('orgId', 'projectId'), user).$promise.then(function () {
                    this.members = _(this.members).without(user);
                });
            };


            this.addPhase = function (newPhase) {
                return Project.api.addPhase(_(this).pick('orgId', 'projectId'), newPhase).$promise.then(angular.bind(this, function (p) {
                    this.phases.push(p);
                    return p;
                }));
            };

            this.updatePhase = function (phase) {
                return this.$updatePhase(_(this).pick('orgId', 'projectId'), phase).$promise.then(angular.bind(this, function () {
                    var existing = _(this.phases).find(function (me) { return me.index === phase.index; });
                    if (existing) {
                        angular.copy(phase, existing);
                    }
                    return existing;
                }));

            };

            this.delPhase = function (oldPhase) {
                return this.$delPhase(_(this).pick('orgId', 'projectId'), oldPhase).$promise.then(angular.bind(this, function () {
                    this.phases = _(this.phases).without(oldPhase);
                }));

            };

            this.getRevision = function (revTime) {
                return _(this.old_revs).find(function (r) { return r.time === revTime; });
            };


            //Will further need methods for members, votes, roles
            //phases, tasks, revisions, and comments

        };

        Project.api = $resource('/api/org/:orgId/project/:projectId', {orgId: '@my_org.unique', projectId: '@unique'}, {
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
        //Need to add Project.api
        //Need to add Project.getbyId
        return Project;
    }];

    return factory;

});