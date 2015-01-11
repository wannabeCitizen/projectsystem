/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore'], function (angular, _) {
    'use strict';

    var factory = {};

    factory.Project = ['$http', '$resource', 'UserSvc', function ($http, $resource, UserSvc) {
        var Project = function (resource) {
            angular.extend(this, resource);

            this.orgId = this.my_org && this.my_org.unique;
            this.projectId = this.unique;
            this.url = '/api/org' + this.orgId + '/project/' + this.projectId;
        };

        Project.prototype.serialize = function () {
            return _(this).pick('title', 'unique', 'short_description', 'based_on', 'budget', 'quorum', 'majority', 'text', 'complete');
        };

        Project.prototype.save = function () {
            return $http.put(this.url, this.serialize())
                .then(angular.bind(this, function (response) {
                    angular.extend(this, response.data);
                    return this;
                }));
        };

        Project.prototype.del = function () {
            return $http.delete(this.url);
        };

        Project.prototype.userIsMember = function (memList) {
            return _(memList).find(function (m) { return UserSvc.isCurrent(m); });
        };

        Project.prototype.userIsFollowing = function () {
            return _(this.followers).find(function (follower) {
                return UserSvc.isCurrentUserId(follower);
            });
        };

        Project.prototype.follow = function () {
            return $http.put(this.url + '/follow').then(angular.bind(this, function () {
                this.followers.push(UserSvc.currentUser.id);
                return this;
            }));
        };

        Project.prototype.unfollow = function () {
            return $http.delete(this.url + '/follow').then(angular.bind(this, function () {
                this.followers = _(this.followers).without(UserSvc.currentUser.id);
                return this;
            }));
        };

        Project.prototype.addRole = function (newRole) {
            return Project.api.addRole(_(this).pick('orgId', 'projectId'), newRole).$promise.then(angular.bind(this, function (r) {
                this.roles.push(r);
                return r;
            }));
        };

        Project.prototype.updateRole = function (role) {
            return this.$updateRole(_(this).pick('orgId', 'projectId'), role).$promise.then(angular.bind(this, function () {
                var existing = _(this.roles).find(function (me) { return me.index === role.index; });
                if (existing) {
                    angular.copy(role, existing);
                }
                return existing;
            }));

        };

        Project.prototype.delRole = function (oldRole) {
            return this.$delRole(_(this).pick('orgId', 'projectId'), oldRole).$promise.then(angular.bind(this, function () {
                this.roles = _(this.roles).without(oldRole);
            }));

        };

        Project.prototype.addTask = function (newTask) {
            return this.$addTask(_(this).pick('orgId', 'projectId'), newTask).$promise.then(angular.bind(this, function (t) {
                this.tasks.push(t);
                return t;
            }));

        };

        Project.prototype.updateTask = function (task) {
            return this.$updateTask(_(this).pick('orgId', 'projectId'), task).$promise.then(angular.bind(this, function () {
                var existing = _(this).find(function (t) { return t.index === task.index; });
                if (existing) {
                    angular.copy(task, existing);
                }
                return existing;
            }));

        };

        Project.prototype.delTask = function (oldTask) {
            return this.$delTask(_(this).pick('orgId', 'projectId'), oldTask).$promise.then(angular.bind(this, function () {
                this.tasks = _(this.tasks).without(oldTask);
            }));

        };

        Project.prototype.addMember = function (user) {
            return this.$addMember(_(this).pick('orgId', 'projectId'), user).$promise.then(function () {
                this.members.push(user);
            });

        };

        Project.prototype.delMember = function (user) {
            return this.$delMember(_(this).pick('orgId', 'projectId'), user).$promise.then(function () {
                this.members = _(this.members).without(user);
            });
        };


        Project.prototype.addPhase = function (newPhase) {
            return Project.api.addPhase(_(this).pick('orgId', 'projectId'), newPhase).$promise.then(angular.bind(this, function (p) {
                this.phases.push(p);
                return p;
            }));
        };

        Project.prototype.updatePhase = function (phase) {
            return this.$updatePhase(_(this).pick('orgId', 'projectId'), phase).$promise.then(angular.bind(this, function () {
                var existing = _(this.phases).find(function (me) { return me.index === phase.index; });
                if (existing) {
                    angular.copy(phase, existing);
                }
                return existing;
            }));

        };

        Project.prototype.delPhase = function (oldPhase) {
            return this.$delPhase(_(this).pick('orgId', 'projectId'), oldPhase).$promise.then(angular.bind(this, function () {
                this.phases = _(this.phases).without(oldPhase);
            }));

        };

        Project.prototype.getRevision = function (revTime) {
            return _(this.old_revs).find(function (r) { return r.time === revTime; });
        };


        //Will further need methods for members, votes, roles
        //phases, tasks, revisions, and comments


        Project.api = $resource('/api/org/:orgId/project/:projectId', {orgId: '@my_org.unique', projectId: '@unique'}, {
            update: { method: 'PUT'},
            addMember: { method: 'PUT', url: '/api/org/:orgId/project/:projectId/member/:userId'},
            delMember: { method: 'DELETE', url: '/api/org/:orgId/project/:projectId/member/:userId'},
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

        Project.getById = function (orgId, projectId) {
            return Project.api.get({orgId: orgId, projectId: projectId}).$promise.then(function (project) {
                return new Project(project);
            });
        };

        return Project;
    }];

    return factory;

});
