/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore', 'moment'], function (angular, _, moment) {
    'use strict';

    var factory = {};

    factory.Idea = ['UserSvc', 'IdeaApi', function (UserSvc, IdeaApi) {
        // This is a class ctor
        return function (resource) {
            var idea = angular.copy(resource, this);

            this.orgId = this.my_org && this.my_org.unique;
            this.ideaId = this.unique;

            _(this.versions).each(function (vers) {
                vers.createdDate = moment(vers.created_on && vers.created_on.$date).format('l LT');
                vers.title = vers.createdDate;
                UserSvc.getById(vers.thinker).then(function (user) {
                    vers.creatorUser = user;
                    vers.title += ' by ' + user.name;
                });
            });

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
