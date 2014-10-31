/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore'], function (angular, _) {
    'use strict';

    var ctrl = {};

    ctrl.NewIdeaCtrl = ['$scope', '$state', '$stateParams', 'Idea', 'MsgSvc',
        function ($scope, $state, $stateParams, Idea, msg) {
            $scope.idea = {};
            $scope.heading = 'Create a new Idea';

            $scope.action = function () {
                $scope.spin = true;
                var newIdea = new Idea.api($scope.idea);
                newIdea.$save({
                    orgId: $stateParams.orgId
                }).then(function (idea) {
                    $state.go('org.idea', {
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

    ctrl.EditIdeaCtrl = ['$scope', '$state', '$stateParams', 'Idea', 'MsgSvc',
        function ($scope, $state, $stateParams, Idea, msg) {
            $scope.heading = 'Edit this Idea';

            Idea.getById($stateParams.orgId, $stateParams.ideaId).then(function (idea) {
                $scope.idea = idea;

                $scope.action = function () {
                    $scope.spin = true;
                    $scope.idea.save().then(function () {
                        $state.go('org.idea', $stateParams);
                    }, function (err) {
                        msg.error('Failed to save the idea.', 'Please try again.');
                    }).finally(function () {
                        $scope.spin = false;
                    });
                };
            }, function (err) {
                msg.error('Failed to load the requested idea.');
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

    ctrl.CommentCtrl = ['$scope', 'MsgSvc', function ($scope, msg) {
        $scope.addComment = function (text) {
            $scope.idea.addComment(text).then(function () {
                $scope.newComment = '';
            }, function () {
                msg.error('Failed to add the comment');
            });
        };

        $scope.delComment = function (comment) {
            $scope.idea.delComment(comment).then(null, function () {
                msg.error('Failed to delete the comment');
            });
        };
    }];

    ctrl.IdeaCtrl = ['$scope', '$state', '$stateParams', 'OrgSvc', 'Idea', 'MsgSvc',
        function ($scope, $state, $stateParams, OrgSvc, Idea, msg) {
            $scope.loading = true;
            $scope.ideaPromise = OrgSvc.getById($stateParams.orgId).then(function (org) {
                $scope.org = org;

                return Idea.getById($stateParams.orgId, $stateParams.ideaId).then(function (idea) {
                    $scope.idea = idea;

                    $scope.delIdea = function () {
                        idea.$delete().then(function () {
                            $state.go('org', {
                                orgId: org.unique
                            });
                        });
                    };

                    return idea;
                }, function (err) {
                    msg.error('Failed to load the specified idea.');
                });
            }, function (err) {
                msg.error('Failed to load the specified organization.');
            }).finally(function () {
                $scope.loading = false;
            });

            $scope.versionClass = function (vers) {
                return {
                    active: vers.versId === $scope.selectedVersId
                };
            };

            $scope.$on('$stateChangeSuccess', function (event, toState, toParams) {
                $scope.isNewVersion = (toState.name === 'org.idea.newVersion');
                $scope.selectedVersId = toParams.versId;
            });
        }];

    // This is a child of IdeaCtrl
    ctrl.NewIdeaVersCtrl = ['$scope', '$state',
        function ($scope, $state) {
            $scope.vers = {};

            $scope.save = function () {
                $scope.spin = true;
                $scope.idea.addVersion($scope.vers).then(function (newVers) {
                    $state.go('org.idea.version', {
                        orgId: $scope.org.unique,
                        ideaId: $scope.idea.unique,
                        versId: newVers.unique
                    });
                }).finally(function () {
                    $scope.spin = false;
                });
            };

            $scope.saveIcon = function () {
                return {
                    fa: true,
                    'fa-spinner': $scope.spin,
                    'fa-spin': $scope.spin,
                    'fa-save-o': !$scope.spin
                };
            };

            $scope.cancel = function () {
                $state.go('org.idea');
            };
        }];

    // This is a child of IdeaCtrl
    ctrl.EditIdeaVersCtrl = ['$scope', '$state', '$stateParams', function ($scope, $state, $stateParams) {
        $scope.versPromise = $scope.ideaPromise.then(function (idea) {
            // we want to edit a copy, not the original directly
            $scope.vers = angular.copy(idea.getVersionById($stateParams.versId));

            $scope.save = function () {
                $scope.spin = true;
                idea.updateVersion($scope.vers).then(function (vers) {
                    $state.go('org.idea.version', {
                        orgId: $scope.idea.orgId,
                        ideaId: $scope.idea.ideaId,
                        versId: vers.versId
                    });
                }).finally(function () {
                    $scope.spin = false;
                });
            };

            $scope.saveIcon = function () {
                return {
                    fa: true,
                    'fa-spinner': $scope.spin,
                    'fa-spin': $scope.spin,
                    'fa-save-o': !$scope.spin
                };
            };

            $scope.cancel = function () {
                $state.go('org.idea.version', $stateParams);
            };

            return $scope.vers;
        });
    }];

    // This is a child of IdeaCtrl
    ctrl.IdeaVersionCtrl = ['$scope', '$state', '$stateParams', 'OrgSvc', 'Idea', 'MsgSvc',
        function ($scope, $state, $stateParams, OrgSvc, Idea, msg) {
            $scope.ideaPromise.then(function (idea) {
                $scope.vers = _(idea.versions).find(function (vers) {
                    return $stateParams.versId === vers.unique;
                });
            });
        }];


    return ctrl;
});
