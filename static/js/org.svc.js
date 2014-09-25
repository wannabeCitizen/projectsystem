/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore'], function (angular, _) {
    'use strict';

    var factory = {};

    factory.Org = ['$q', 'OrgApi', 'UserSvc', function ($q, OrgApi, UserSvc) {
        // This is a class ctor
        return function (resource) {
            var org = angular.copy(resource, this);

            org.ownersList = resource.owners;
            UserSvc.getList(resource.owners).then(function (list) {
                org.owners = list;
            });

            org.membersList = resource.members;
            UserSvc.getList(resource.members).then(function (list) {
                org.members = list;
            });

            org.userInList = function (list) {
                return _(list).find(function (u) { return UserSvc.isCurrentUser(u); });
            };

            org.userIsOwner = function () {
                return org.userInList(org.owners);
            };

            org.userIsMember = function () {
                return org.userIsOwner() || org.userInList(org.members);
            };

            org.addOwner = function (user) {
                OrgApi.addOwner({orgId: org.unique}, user).$promise.then(function () {
                    org.owners.push(user);
                });
            };

            org.delOwner = function (user) {
                if (org.owners.length === 1) {
                    return $q.reject('You cannot delete the only owner. Add a new owner first.');
                }
                return OrgApi.delOwner({orgId: org.unique, userId: user.google_id}).$promise.then(function () {
                    org.owners = _(org.owners).without(user);
                });
            };

            org.addMember = function (user) {
                return OrgApi.addMember({orgId: org.unique}, user).$promise.then(function () {
                    org.members.push(user);
                });
            };

            org.delMember = function (user) {
                return OrgApi.delMember({orgId: org.unique, userId: user.google_id}).$promise.then(function () {
                    org.members = _(org.members).without(user);
                });
            };
        };
    }];

    factory.OrgSvc = ['Org', 'OrgApi', function (Org, OrgApi) {
        var svc = {};

        svc.getAll = function () {
            return OrgApi.query().$promise.then(function (orgs) {
                return _(orgs).map(function (org) { return new Org(org); });
            });
        };

        svc.getById = function (orgId) {
            return OrgApi.get({orgId: orgId}).$promise.then(function (org) {
                return new Org(org);
            });
        };

        return svc;
    }];

    return factory;
});
