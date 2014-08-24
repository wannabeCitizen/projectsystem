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

    ctrl.NewOrgCtrl = ['$scope', '$state', 'OrgApi', 'MessageSvc',
        function ($scope, $state, OrgApi, msg) {
            $scope.org = {};

            $scope.formStyle = function (name) {
                return {
                    'has-error': $scope.orgForm[name].$invalid && $scope.orgForm[name].$dirty,
                    'has-success': $scope.orgForm[name].$valid && $scope.orgForm[name].$dirty
                };
            };


            $scope.create = function () {
                $scope.createSpin = true;
                var neworg = new OrgApi($scope.org);
                neworg.$save().then(function (org) {
                    $state.go('org', {
                        id: org.unique
                    });
                }, function (err) {
                    msg.debug(err);
                    $scope.errMsg = 'Failed to create the organization. Try again.';
                }).finally(function () {
                    $scope.createSpin = false;
                });
            };
        }];

    return ctrl;
});