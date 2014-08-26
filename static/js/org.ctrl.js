/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore'], function (angular, _) {
    'use strict';

    var ctrl = {};

    // Works with the list of orgs
    ctrl.OrgsCtrl = ['$scope', 'OrgSvc', 'MsgSvc',
        function ($scope, OrgSvc, msg) {
            OrgSvc.getAll().then(function (orgs) {
                $scope.list = orgs;
            }, function (err) {
                msg.error('Failed to load the list of organizations.');
            });
        }];

    ctrl.OrgCtrl = ['$scope', '$state', '$stateParams', 'OrgSvc', 'UserSvc', 'MsgSvc',
        function ($scope, $state, $stateParams, OrgSvc, UserSvc, msg) {
            $scope.loading = true;
            OrgSvc.getById($stateParams.orgId).then(function (org) {
                $scope.org = org;
            }, function (err) {
                msg.error('Failed to load the specified organization.');
            }).finally(function () {
                $scope.loading = false;
            });

            $scope.ownerToAdd = '';
            $scope.memberToAdd = '';

            $scope.addOwner = function () {
                $scope.org.addOwner($scope.ownerToAdd).then(null, function (err) {
                    msg.error('Failed to add a new owner.');
                }).finally(function () {
                    $scope.showAddOwn = false;
                    $scope.ownerToAdd = '';
                });
            };

            $scope.delOwner = function (user) {
                $scope.org.delOwner(user).$promise.then(null, function (err) {
                    msg.error('Failed to delete the specified owner.', typeof err === 'string' ? err : user.name);
                });
            };

            $scope.addMember = function () {
                $scope.org.addMember($scope.memberToAdd).then(null, function (err) {
                    msg.error('Failed to add a new member.');
                }).finally(function () {
                    $scope.showAddMember = false;
                    $scope.memberToAdd = '';
                });
            };

            $scope.delMember = function (user) {
                $scope.org.delMember(user).then(null, function (err) {
                    msg.error('Failed to delete the specified member.', user.name);
                });
            };

            $scope.canAddUser = function (user, group) {
                return user && user.google_id && !_(group).find(function (u) { return UserSvc.usersEqual(u, user); });
            };

            $scope.delOrg = function () {
                $scope.org.$delete().then(function () {
                    msg.success('The organization was deleted.');
                    $state.go('orgs');
                }, function (err) {
                    msg.error('Failed to delete the organization.');
                });
            };
        }];

    ctrl.NewOrgCtrl = ['$scope', '$state', 'OrgApi', 'MsgSvc',
        function ($scope, $state, OrgApi, msg) {
            $scope.org = {};
            $scope.heading = 'Create a new Organization';

            $scope.actionLabel = 'Create';
            $scope.action = function () {
                $scope.spin = true;
                var neworg = new OrgApi($scope.org);
                neworg.$save().then(function (org) {
                    $state.go('org', {
                        orgId: org.unique
                    });
                }, function (err) {
                    msg.error('Failed to create the organization.', 'Please try again.');
                }).finally(function () {
                    $scope.spin = false;
                });
            };

            $scope.actionIcon = function () {
                return {
                    fa: true,
                    'fa-spinner': $scope.spin,
                    'fa-spin': $scope.spin,
                    'fa-plus': !$scope.spin
                };
            };
        }];

    ctrl.EditOrgCtrl = ['$scope', '$state', '$stateParams', 'OrgSvc', 'MsgSvc',
        function ($scope, $state, $stateParams, OrgSvc, msg) {
            $scope.heading = 'Edit this Organization';

            OrgSvc.getById($stateParams.orgId).then(function (org) {
                $scope.org = org;

                $scope.action = function () {
                    $scope.spin = true;
                    $scope.org.$update().then(function (o) {
                        $state.go('org', {
                            orgId: o.unique
                        });
                    }, function (err) {
                        msg.error('Failed to save the organization.', 'Please try again.');
                    }).finally(function () {
                        $scope.spin = false;
                    });
                };
            }, function (err) {
                msg.error('Failed to load the requested organization.');
            }).finally(function () {
                $scope.loading = false;
            });

            $scope.actionLabel = 'Save';
            $scope.actionIcon = function () {
                return {
                    fa: true,
                    'fa-spinner': $scope.spin,
                    'fa-spin': $scope.spin,
                    'fa-save-o': !$scope.spin
                };
            };
        }];

    return ctrl;
});
