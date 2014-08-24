/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var ctrl = {};

    // Works with the list of orgs
    ctrl.OrgsCtrl = ['$scope', 'OrgApi', 'MessageSvc',
        function ($scope, OrgApi, msg) {
            OrgApi.query().$promise.then(function (orgs) {
                $scope.list = orgs;
            }, function (err) {
                msg.debug(err);
            });
        }];

    ctrl.OrgCtrl = ['$scope', '$stateParams', 'OrgApi', 'MessageSvc',
        function ($scope, $stateParams, OrgApi, msg) {
            $scope.loading = true;
            OrgApi.get({
                orgId: $stateParams.id
            }).$promise.then(function (org) {
                $scope.org = org;
            }, function (err) {
                msg.debug(err);
            }).finally(function () {
                $scope.loading = false;
            });
        }];

    var orgFormStyle = function (name, $scope) {
        return {
            'has-error': $scope.orgForm[name].$invalid && $scope.orgForm[name].$dirty,
            'has-success': $scope.orgForm[name].$valid && $scope.orgForm[name].$dirty
        };
    };

    ctrl.NewOrgCtrl = ['$scope', '$state', 'OrgApi', 'MessageSvc',
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
                    msg.debug(err);
                    $scope.errMsg = 'Failed to create the organization. Try again.';
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

    ctrl.EditOrgCtrl = ['$scope', '$state', '$stateParams', 'OrgApi', 'MessageSvc',
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
                        msg.debug(err);
                        $scope.errMsg = 'Failed to save the organization. Try again.';
                    }).finally(function () {
                        $scope.spin = false;
                    });
                };
            }, function (err) {
                msg.debug(err);
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
