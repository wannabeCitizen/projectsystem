/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore'], function (angular, _) {
    'use strict';

    var factory = {};

    factory.Idea = ['UserSvc', function (UserSvc) {
        // This is a class ctor
        return function (resource) {
            var idea = angular.copy(resource, this);

            this.userIsFollowing = function () {
                return _(this.followers).find(function (follower) {
                    return UserSvc.isCurrentUserId(follower);
                });
            };

            this.follow = function () {
                this.$follow().then(function () {
                    idea.followers.push(UserSvc.currentUser.id);
                });
            };

            this.unfollow = function () {
                this.$unfollow().then(function () {
                    idea.followers = _(idea.followers).without(UserSvc.currentUser.id);
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
