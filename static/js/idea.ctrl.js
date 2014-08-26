/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore'], function (angular, _) {
    'use strict';

    var ctrl = {};

    ctrl.NewIdeaCtrl = ['$scope', '$state', '$stateParams', 'IdeaApi', 'MsgSvc',
        function ($scope, $state, $stateParams, IdeaApi, msg) {
            $scope.idea = {};

            $scope.action = function () {
                $scope.spin = true;
                var newIdea = new IdeaApi($scope.idea);
                newIdea.$save({orgId: $stateParams.orgId}).then(function (idea) {
                    $state.go('idea', {
                        orgId: $stateParams.orgId,
                        ideaId: idea.unique
                    });
                }, function (err) {
                    msg.error('Failed to create the idea.', 'Please try again.');
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

    ctrl.IdeaCtrl = ['$scope', '$state', '$stateParams', 'OrgSvc', 'IdeaSvc', 'MsgSvc',
        function ($scope, $state, $stateParams, OrgSvc, IdeaSvc, msg) {
            $scope.loading = true;
            OrgSvc.getById($stateParams.orgId).then(function (org) {
                $scope.org = org;

                return IdeaSvc.getById($stateParams.orgId, $stateParams.ideaId).then(function (idea) {
                    $scope.idea = idea;
                }, function (err) {
                    msg.error('Failed to load the specified idea.');
                });
            }, function (err) {
                msg.error('Failed to load the specified organization.');
            }).finally(function () {
                $scope.loading = false;
            });
        }];


    return ctrl;
});
