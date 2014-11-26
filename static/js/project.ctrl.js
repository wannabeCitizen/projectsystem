/*jslint browser:true, nomen:true*/
/*global define */

define(['angular', 'underscore'], function (angular, _) {
    'use strict';

    var ctrl = {};

    ctrl.ProjectCtrl = ['$scope', '$state', '$stateParams', 'Org', 'Project', 'MsgSvc',
        function ($scope, $state, $stateParams, Org, Project, msg) {
            $scope.loading = true;
            $scope.projectPromise = Org.getById($stateParams.orgId).then(function (org) {
                $scope.org = org;

                return Project.getById($stateParams.orgId, $stateParams.projectId).then(function (project) {
                    $scope.project = project;

                    $scope.delProject = function () {
                        project.del().then(function () {
                            $state.go('org', {
                                orgId: org.unique
                            });
                        });
                    };

                    return project;

                }, function (err) {
                    msg.error('Failed to load the specified project.');
                });
            }, function (err) {
                msg.error('Failed to load the specified organization.');
            }).finally(function () {
                $scope.loading = false;
            });
        }];

    ctrl.NewProjectCtrl = ['$scope', '$state', '$stateParams', 'Project', 'MsgSvc',
        function ($scope, $state, $stateParams, Project, msg) {
            $scope.projectToEdit = {};
            $scope.heading = 'Start a new Project!';

            $scope.action = function () {
                $scope.spin = true;
                var newProject = Project.api($scope.projectToEdit);
                newProject.$save({
                    orgId: $stateParams.orgId
                }).then(function (project) {
                    $state.go('org.project', {
                        orgId: $stateParams.orgId,
                        projectId: project.unique
                    });
                }, function (err) {
                    msg.error('Failed to create the project.', 'Please try again.');
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

    ctrl.EditProjectCtrl = ['$scope', '$state', '$stateParms', 'Project', 'MsgSvc',
        function ($scope, $state, $stateParams, Project, msg) {
            $scope.heading = 'Edit this Project!';

            $scope.projectPromise.then(function (project) {
                $scope.projectToEdit = angular.copy(project);
            });

            $scope.action = function () {
                $scope.spin = true;
                $scope.projectToEdit.save().then(function () {
                    angular.copy($scope.projecToEdit, $scope.project);
                    $state.go('org.project', $stateParams);
                }, function (err) {
                    msg.error('Failed to save the project.', 'Please try again.');
                }).finally(function () {
                    $scope.spin = false;
                });
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