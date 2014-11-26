/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore', 'moment'], function (angular, _, moment) {
    'use strict';

    var factory = {};

    factory.Version = ['$http', 'UserSvc', function ($http, UserSvc) {
        // Instance ctor
        var Version = function (resource, idea) {
            angular.extend(this, resource);

            this.versId = this.unique;
            this.url = '/api/org/' + idea.orgId + '/idea/' + idea.ideaId + '/version/' + this.versId;
            this.createdDate = moment.utc(this.created_on && this.created_on.$date).format('l LT');
            this.title = this.createdDate;
            this.$promise = UserSvc.getById(this.thinker).then(angular.bind(this, function (user) {
                this.creatorUser = user;
                this.title += ' by ' + user.name;
            }));

            this.serialize = function () {
                return _(this).pick('thinker', 'text', 'unique');
            };

            this.save = function () {
                return $http.put(this.url, this.serialize()).then(
                    angular.bind(this, function (response) {
                        angular.extend(this, response.data);
                        return this;
                    })
                );
            };
        };

        return Version;
    }];

    factory.Comment = ['$http', 'UserSvc', function ($http, UserSvc) {
        var Comment = function (resource, baseUrl) {
            angular.extend(this, resource);

            this.baseUrl = baseUrl;
            this.commentId = this.index;
            this.url = baseUrl + '/' + this.commentId;
            this.date = moment.utc(this.time && this.time.$date).format('l LT');
            this.$promise = UserSvc.getById(this.commenter).then(angular.bind(this, function (user) {
                this.user = user;
            }));
        };

        Comment.prototype.serialize = function () {
            return _(this).pick('commenter', 'text', 'time', 'replies', 'num_replies', 'index');
        };

        Comment.prototype.save = function () {
            return $http.put(this.url, this.serialize())
                .then(angular.bind(this, function (response) {
                    angular.extend(this, new Comment(response.data, this.baseUrl));
                    return this;
                }));
        };

        Comment.prototype.del = function () {
            return $http.delete(this.url)
                .then(angular.bind(this, function (response) {
                    angular.extend(this, new Comment(response.data, this.baseUrl));
                    return this;
                }));
        };

        Comment.prototype.userIsAuthor = function () {
            return UserSvc.isCurrentUser(this.user);
        };

        return Comment;
    }];

    factory.Idea = ['$http', '$resource', 'UserSvc', 'Version', 'Comment', function ($http, $resource, UserSvc, Version, Comment) {
        // Instance ctor
        var Idea = function (resource) {
            angular.extend(this, resource);

            this.orgId = this.my_org && this.my_org.unique;
            this.ideaId = this.unique;
            this.url = '/api/org/' + this.orgId + '/idea/' + this.ideaId;
            this.commentUrl = this.url + '/comment';

            _(this.versions).each(function (vers, i) {
                this.versions[i] = new Version(vers, this);
            }, this);
            this.versions = this.versions || [];

            _(this.comments).each(function (vers, i) {
                this.comments[i] = new Comment(vers, this.commentUrl);
            }, this);
            this.comments = this.comments || [];

            this.serialize = function () {
                return _(this).pick('title', 'short_description', 'unique');
            };

            this.save = function () {
                return $http.put(this.url, this.serialize()).then(
                    angular.bind(this, function (response) {
                        angular.extend(this, response.data);
                        return this;
                    })
                );
            };

            this.del = function () {
                return $http.delete(this.url);
            };

            this.userIsFollowing = function () {
                return _(this.followers).find(function (follower) {
                    return UserSvc.isCurrentUserId(follower);
                });
            };

            this.follow = function () {
                $http.put(this.url + '/follow').then(angular.bind(this, function () {
                    this.followers.push(UserSvc.currentUser.id);
                    return this;
                }));
            };

            this.unfollow = function () {
                $http.delete(this.url + '/follow').then(angular.bind(this, function () {
                    this.followers = _(this.followers).without(UserSvc.currentUser.id);
                    return this;
                }));
            };

            this.addVersion = function (versData) {
                return Idea.api.addVersion(_(this).pick('orgId', 'ideaId'), versData).$promise.then(angular.bind(this, function (newVers) {
                    var vers = new Version(newVers, this);
                    this.versions.push(vers);
                    return vers;
                }));
            };

            this.updateVersion = function (vers) {
                return vers.save().then(angular.bind(this, function () {
                    var existing = _(this.versions).find(function (v) { return v.versId === vers.versId; });
                    if (existing) {
                        angular.copy(vers, existing);
                    }
                    return existing;
                }));
            };

            this.getVersionById = function (versId) {
                return _(this.versions).find(function (vers) { return vers.unique === versId; });
            };

            this.addComment = function (text) {
                return Idea.api.addComment(_(this).pick('orgId', 'ideaId'), {text: text}).$promise
                    .then(angular.bind(this, function (comment) {
                        var c = new Comment(comment, this.commentUrl);
                        this.comments.push(c);
                    }));
            };

            this.delComment = function (comment) {
                return comment.del();
            };
        };

        Idea.api = $resource('/api/org/:orgId/idea/:ideaId', {orgId: '@my_org.unique', ideaId: '@unique'}, {
            update: { method: 'PUT' },
            addVersion: { method: 'POST' },
            updateVersion: { method: 'PUT', url: '/api/org/:orgId/idea/:ideaId/version/:versId' },
            addComment: { method: 'POST', url: '/api/org/:orgId/idea/:ideaId/comment' }
        });

        Idea.getById = function (orgId, ideaId) {
            return Idea.api.get({orgId: orgId, ideaId: ideaId}).$promise.then(function (idea) {
                return new Idea(idea);
            });
        };

        return Idea;
    }];

    return factory;
});
