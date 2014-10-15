/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore', 'moment'], function (angular, _, moment) {
    'use strict';

    var factory = {};

    factory.Version = ['UserSvc', function (UserSvc) {
        // Instance ctor
        var Version = function (resource) {
            angular.extend(this, resource);

            this.createdDate = moment(this.created_on && this.created_on.$date).format('l LT');
            this.title = this.createdDate;
            this.$promise = UserSvc.getById(this.thinker).then(angular.bind(this, function (user) {
                this.creatorUser = user;
                this.title += ' by ' + user.name;
            }));
        };

        return Version;
    }];

    factory.Idea = ['UserSvc', 'IdeaApi', 'Version', function (UserSvc, IdeaApi, Version) {
        // Instance ctor
        var Idea = function (resource) {
            angular.extend(this, resource);

            this.orgId = this.my_org && this.my_org.unique;
            this.ideaId = this.unique;

            _(this.versions).each(function (vers, i) {
                this.versions[i] = new Version(vers);
            }, this);

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

            this.addVersion = function (versData) {
                return IdeaApi.addVersion(_(this).pick('orgId', 'ideaId'), versData).$promise.then(angular.bind(this, function (newVers) {
                    var vers = new Version(newVers);
                    this.versions.push(vers);
                    return vers;
                }));
            };
        };

        return Idea;
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
