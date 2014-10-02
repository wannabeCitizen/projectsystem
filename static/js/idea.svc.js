/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore'], function (angular, _) {
    'use strict';

    var factory = {};

    factory.Idea = ['UserSvc', 'IdeaApi', function (UserSvc, IdeaApi) {
        // This is a class ctor
        return function (resource) {
            var idea = angular.copy(resource, this);

            this.orgId = this.my_org && this.my_org.unique;
            this.ideaId = this.unique;

            this.userIsFollowing = function () {
                return _(this.followers).find(function (follower) {
                    return UserSvc.isCurrentUserId(follower);
                });
            };

            this.follow = function () {
                return this.$follow().then(function () {
                    idea.followers.push(UserSvc.currentUser.id);
                    return idea;
                });
            };

            this.unfollow = function () {
                return this.$unfollow().then(function () {
                    idea.followers = _(idea.followers).without(UserSvc.currentUser.id);
                    return idea;
                });
            };

            this.addVersion = function (versData) {
                return IdeaApi.addVersion(_(this).pick('orgId', 'ideaId'), versData).$promise.then(function (newVers) {
                    idea.versions.push(newVers);
                    return newVers;
                });
            };

            return idea;
        };
    }];

    factory.IdeaSvc = ['Idea', 'IdeaApi', function (Idea, IdeaApi) {
        var svc = {};

        svc.getById = function (orgId, ideaId) {
            return IdeaApi.get({orgId: orgId, ideaId: ideaId}).$promise.then(function (idea) {
                return new Idea(idea);
            });
        };

        return svc;
    }];

    return factory;
});
