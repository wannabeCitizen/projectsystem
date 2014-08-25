/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore'], function (angular, _) {
    'use strict';

    var ctrl = {};

    // Works with the list of orgs
    ctrl.OrgsCtrl = ['$scope', 'OrgApi', 'MsgSvc',
        function ($scope, OrgApi, msg) {
            OrgApi.query().$promise.then(function (orgs) {
                $scope.list = orgs;
            }, function (err) {
                msg.error('Failed to load the list of organizations.');
            });
        }];

    ctrl.OrgCtrl = ['$scope', '$stateParams', 'OrgApi', 'UserSvc', 'MsgSvc',
        function ($scope, $stateParams, OrgApi, UserSvc, msg) {
            $scope.loading = true;
            OrgApi.get({
                orgId: $stateParams.id
            }).$promise.then(function (org) {
                $scope.org = org;
                $scope.userIsOwner = function () { return _(org.owners).find(function (u) { return UserSvc.isCurrentUser(u); }); };
            }, function (err) {
                msg.error('Failed to load the specified organization.');
            }).finally(function () {
                $scope.loading = false;
            });

            $scope.ownerToAdd = '';
            $scope.memberToAdd = '';

            $scope.addOwner = function () {
                OrgApi.addOwner({orgId: $scope.org.unique}, $scope.ownerToAdd).$promise.then(function () {
                    $scope.org.owners.push($scope.ownerToAdd);
                }, function (err) {
                    msg.error('Failed to add a new owner.');
                }).finally(function () {
                    $scope.showAddOwn = false;
                    $scope.ownerToAdd = '';
                });
            };
            $scope.delOwner = function (user) {
                if ($scope.org.owners.length <= 1) {
                    msg.error('You cannot delete the only owner.', 'Add a new owner first.');
                    return;
                }
                OrgApi.delOwner({orgId: $scope.org.unique, userId: user.google_id}).$promise.then(function () {
                    $scope.org.owners = _($scope.org.owners).without(user);
                }, function (err) {
                    msg.error('Failed to delete the specified owner.', user.name);
                });
            };
            $scope.addMember = function () {
                OrgApi.addMember({orgId: $scope.org.unique}, $scope.memberToAdd).$promise.then(function () {
                    $scope.org.members.push($scope.memberToAdd);
                }, function (err) {
                    msg.error('Failed to add a new member.');
                }).finally(function () {
                    $scope.showAddMember = false;
                    $scope.memberToAdd = '';
                });
            };
            $scope.delMember = function (user) {
                OrgApi.delMember({orgId: $scope.org.unique, userId: user.google_id}).$promise.then(function () {
                    $scope.org.members = _($scope.org.members).without(user);
                }, function (err) {
                    msg.error('Failed to delete the specified member.', user.name);
                });
            };
            $scope.canAddUser = function (user, group) {
                return user && user.google_id && !_(group).find(function (u) { return UserSvc.usersEqual(u, user); });
            };
        }];

    var orgFormStyle = function (name, $scope) {
        return {
            'has-error': $scope.orgForm[name].$invalid && $scope.orgForm[name].$dirty,
            'has-success': $scope.orgForm[name].$valid && $scope.orgForm[name].$dirty
        };
    };

    ctrl.NewOrgCtrl = ['$scope', '$state', 'OrgApi', 'MsgSvc',
        function ($scope, $state, OrgApi, msg) {
            $scope.org = {};
            $scope.heading = 'Create a new Organization';

            $scope.formStyle = function (name) {
                return orgFormStyle(name, $scope);
            };

            $scope.actionLabel = 'Create';
            $scope.action = function () {
                $scope.spin = true;
                var neworg = new OrgApi($scope.org);
                neworg.$save().then(function (org) {
                    $state.go('org', {
                        id: org.unique
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

    ctrl.EditOrgCtrl = ['$scope', '$state', '$stateParams', 'OrgApi', 'MsgSvc',
        function ($scope, $state, $stateParams, OrgApi, msg) {
            $scope.heading = 'Edit this Organization';

            OrgApi.get({
                orgId: $stateParams.id
            }).$promise.then(function (org) {
                $scope.org = org;

                $scope.action = function () {
                    $scope.spin = true;
                    $scope.org.$update().then(function (o) {
                        $state.go('org', {
                            id: o.unique
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

            $scope.formStyle = function (name) {
                return orgFormStyle(name, $scope);
            };

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
