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
        };

        Version.prototype.serialize = function () {
            return _(this).pick('thinker', 'text', 'unique');
        };

        Version.prototype.save = function () {
            return $http.put(this.url, this.serialize()).then(
                angular.bind(this, function (response) {
                    angular.extend(this, response.data);
                    return this;
                })
            );
        };

        Version.prototype.hasUserKarma = function () {
            return _(this.karmaUsers).contains(UserSvc.currentUser.id);
        };

        return Version;
    }];

    factory.Comment = ['$http', 'UserSvc', 'Reply', function ($http, UserSvc, Reply) {
        var Comment = function (resource, baseUrl) {
            angular.extend(this, resource);

            this.baseUrl = baseUrl;
            this.commentId = this.index;
            this.url = baseUrl + '/' + this.commentId;
            this.replyUrl = this.url + '/reply';
            this.date = moment.utc(this.time && this.time.$date).format('l LT');
            this.$promise = UserSvc.getById(this.commenter).then(angular.bind(this, function (user) {
                this.user = user;
            }));

            _(this.replies).each(function (reply, i) {
                this.replies[i] = new Reply(reply, this.replyUrl);
            }, this);
            this.replies = this.replies || [];
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

        Comment.prototype.addReply = function (text) {
            return $http.post(this.replyUrl, {text: text}).then(angular.bind(this, function (response) {
                var reply = new Reply(response.data, this.replyUrl);
                this.replies.push(reply);
                return reply;
            }));
        };

        return Comment;
    }];

    factory.Reply = ['$http', 'UserSvc', function ($http, UserSvc) {
        var Reply = function (resource, baseUrl) {
            angular.extend(this, resource);

            this.baseUrl = baseUrl;
            this.replyId = this.index;
            this.url = baseUrl + '/' + this.replyId;
            this.date = moment.utc(this.time && this.time.$date).format('l LT');
            this.$promise = UserSvc.getById(this.replier).then(angular.bind(this, function (user) {
                this.user = user;
            }));
        };

        Reply.prototype.serialize = function () {
            return _(this).pick('replier', 'text', 'time', 'index');
        };

        Reply.prototype.save = function () {
            return $http.put(this.url, this.serialize())
                .then(angular.bind(this, function (response) {
                    angular.extend(this, new Reply(response.data, this.baseUrl));
                    return this;
                }));
        };

        Reply.prototype.del = function () {
            return $http.delete(this.url)
                .then(angular.bind(this, function (response) {
                    angular.extend(this, new Reply(response.data, this.baseUrl));
                    return this;
                }));
        };

        Reply.prototype.userIsAuthor = function () {
            return UserSvc.isCurrentUser(this.user);
        };

        return Reply;
    }];

    factory.Idea = ['$http', 'UserSvc', 'Version', 'Comment', function ($http, UserSvc, Version, Comment) {

        var updateVersKarma = function (vers, ideaKarma) {
            vers.karmaUsers = [];
            _(ideaKarma).each(function (v, u) {
                if (v === vers.versId) {
                    vers.karmaUsers.push(u);
                }
            });
            vers.karma = vers.karmaUsers && vers.karmaUsers.length;
        };

        // Instance ctor
        var Idea = function (resource, orgId) {
            angular.extend(this, resource);

            this.orgId = orgId || (this.my_org && this.my_org.unique);
            this.ideaId = this.unique || '';
            this.url = '/api/org/' + this.orgId + '/idea/' + this.ideaId;
            this.commentUrl = this.url + '/comment';

            this.karma = this.karma || {};

            _(this.versions).each(function (v, i) {
                this.versions[i] = new Version(v, this);
                updateVersKarma(this.versions[i], this.karma);
            }, this);
            this.versions = this.versions || [];

            _(this.comments).each(function (vers, i) {
                this.comments[i] = new Comment(vers, this.commentUrl);
            }, this);
            this.comments = this.comments || [];
        };

        Idea.prototype.serialize = function () {
            return _(this).pick('title', 'short_description', 'unique');
        };

        Idea.prototype.save = function () {
            return $http.put(this.url, this.serialize()).then(
                angular.bind(this, function (response) {
                    angular.extend(this, new Idea(response.data));
                    return this;
                })
            );
        };

        Idea.prototype.del = function () {
            return $http.delete(this.url);
        };

        Idea.prototype.userIsFollowing = function () {
            return _(this.followers).find(function (follower) {
                return UserSvc.isCurrentUserId(follower);
            });
        };

        Idea.prototype.follow = function () {
            return $http.put(this.url + '/follow').then(angular.bind(this, function () {
                this.followers.push(UserSvc.currentUser.id);
                return this;
            }));
        };

        Idea.prototype.unfollow = function () {
            return $http.delete(this.url + '/follow').then(angular.bind(this, function () {
                this.followers = _(this.followers).without(UserSvc.currentUser.id);
                return this;
            }));
        };

        Idea.prototype.addVersion = function (versData) {
            return $http.post(this.url, versData).then(angular.bind(this, function (response) {
                var vers = new Version(response.data, this);
                this.versions.push(vers);
                return vers;
            }));
        };

        Idea.prototype.updateVersion = function (vers) {
            return vers.save().then(angular.bind(this, function () {
                var existing = _(this.versions).find(function (v) { return v.versId === vers.versId; });
                if (existing) {
                    angular.copy(vers, existing);
                }
                return existing;
            }));
        };

        Idea.prototype.getVersionById = function (versId) {
            return _(this.versions).find(function (vers) { return vers.unique === versId; });
        };

        Idea.prototype.addComment = function (text) {
            return $http.post(this.url + '/comment', {text: text})
                .then(angular.bind(this, function (response) {
                    var c = new Comment(response.data, this.commentUrl);
                    this.comments.push(c);
                }));
        };

        Idea.prototype.delComment = function (comment) {
            return comment.del();
        };

        Idea.prototype.grantKarma = function (vers) {
            return $http.put(this.url + '/karma/' + vers.versId).then(angular.bind(this, function (response) {
                angular.copy(response.data, this.karma);
                // recompute the karma counts
                _(this.versions).each(function (vers) {
                    updateVersKarma(vers, this.karma);
                }, this);
            }));
        };

        // Static

        Idea.createNew = function (orgId, data) {
            return $http.post('/api/org/' + orgId + '/idea', data).then(function (response) {
                return new Idea(response.data);
            });
        };

        Idea.getById = function (orgId, ideaId) {
            return $http.get('/api/org/' + orgId + '/idea/' + ideaId).then(function (response) {
                return new Idea(response.data);
            });
        };

        return Idea;
    }];

    return factory;
});
