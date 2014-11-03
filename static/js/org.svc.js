/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore'], function (angular, _) {
    'use strict';

    var factory = {};

    factory.Org = ['$q', '$http', 'UserSvc', function ($q, $http, UserSvc) {
        // This is a class ctor
        var Org = function (resource) {
            angular.extend(this, resource);

            this.orgId = resource.unique;
            this.url = Org.url + this.orgId;

            this.owners = [];
            if (resource.owners) {
                this.ownersList = resource.owners;
                UserSvc.getList(resource.owners).then(angular.bind(this, function (list) {
                    this.owners = list;
                }));
            }

            this.members = [];
            if (resource.members) {
                this.membersList = resource.members;
                UserSvc.getList(resource.members).then(angular.bind(this, function (list) {
                    this.members = list;
                }));
            }

            this.userInList = function (list) {
                return _(list).find(function (u) { return UserSvc.isCurrentUser(u); });
            };

            this.userIsOwner = function () {
                return this.userInList(this.owners);
            };

            this.userIsMember = function () {
                return this.userIsOwner() || this.userInList(this.members);
            };

            this.addOwner = function (user) {
                return $http.put(this.url + '/owner/' + user.google_id).then(angular.bind(this, function () {
                    this.owners.push(user);
                }));
            };

            this.delOwner = function (user) {
                if (this.owners.length === 1) {
                    return $q.reject('You cannot delete the only owner. Add a new owner first.');
                }
                return $http.delete(this.url + '/owner/' + user.google_id).then(angular.bind(this, function () {
                    this.owners = _(this.owners).without(user);
                }));
            };

            this.addMember = function (user) {
                return $http.put(this.url + '/member/' + user.google_id).then(angular.bind(this, function () {
                    this.members.push(user);
                }));
            };

            this.delMember = function (user) {
                return $http.delete(this.url + '/member/' + user.google_id).then(angular.bind(this, function () {
                    this.members = _(this.members).without(user);
                }));
            };

            this.update = function () {
                return $http.put(this.url, this).then(angular.bind(this, function (response) {
                    return angular.extend(this, response.data);
                }));
            };
        };

        Org.url = '/api/org/';

        Org.create = function (data) {
            return $http.post(Org.url, data).then(function (response) {
                return new Org(response.data);
            });
        };

        Org.getAll = function () {
            return $http.get(Org.url).then(function (response) {
                return _(response.data).map(function (org) { return new Org(org); });
            });
        };

        Org.getById = function (orgId) {
            return $http.get(Org.url + orgId).then(function (response) {
                return new Org(response.data);
            });
        };

        return Org;
    }];

    return factory;
});
