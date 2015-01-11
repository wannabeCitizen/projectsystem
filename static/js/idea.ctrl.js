/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore'], function (angular, _) {
    'use strict';

    var ctrl = {};

    ctrl.IdeaCtrl = ['$scope', '$state', '$stateParams', 'Org', 'Idea', 'MsgSvc',
        function ($scope, $state, $stateParams, Org, Idea, msg) {
            $scope.loading = true;
            $scope.ideaPromise = Org.getById($stateParams.orgId).then(function (org) {
                $scope.org = org;

                return Idea.getById($stateParams.orgId, $stateParams.ideaId).then(function (idea) {
                    $scope.idea = idea;

                    $scope.delIdea = function () {
                        idea.del().then(function () {
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
    ctrl.NewIdeaCtrl = ['$scope', '$state', '$stateParams', 'Idea', 'MsgSvc',
        function ($scope, $state, $stateParams, Idea, msg) {
            $scope.ideaToEdit = {};
            $scope.heading = 'Create a new Idea';

            $scope.action = function () {
                $scope.spin = true;
                Idea.createNew($stateParams.orgId, $scope.ideaToEdit).then(function (idea) {
                    $state.go('org.idea', {
                        orgId: idea.orgId,
                        ideaId: idea.ideaId
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

    // This is a child of IdeaCtrl
    ctrl.EditIdeaCtrl = ['$scope', '$state', '$stateParams', 'Idea', 'MsgSvc',
        function ($scope, $state, $stateParams, Idea, msg) {
            $scope.heading = 'Edit this Idea';

            $scope.ideaPromise.then(function (idea) {
                $scope.ideaToEdit = angular.copy(idea);
            });

            $scope.action = function () {
                $scope.spin = true;
                $scope.ideaToEdit.save().then(function () {
                    angular.copy($scope.ideaToEdit, $scope.idea);
                    $state.go('org.idea', $stateParams);
                }, function (err) {
                    msg.error('Failed to save the idea.', 'Please try again.');
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

    ctrl.CommentCtrl = ['$scope', 'MsgSvc', function ($scope, msg) {
        $scope.addComment = function (text) {
            $scope.idea.addComment(text).then(function () {
                $scope.newComment = '';
                $scope.idea.commenting = false;
            }, function () {
                msg.error('Failed to add the comment');
            });
        };

        $scope.delComment = function (comment) {
            $scope.idea.delComment(comment).then(null, function () {
                msg.error('Failed to delete the comment');
            });
        };

        $scope.editComment = function (comment) {
            comment.$editClone = angular.copy(comment);
        };

        $scope.cancelCommentEdit = function (comment) {
            comment.$editClone = null;
        };

        $scope.saveCommentEdit = function (comment) {
            comment.$editClone.save().then(function (c) {
                angular.copy(c, comment);
            });
        };

        $scope.addReply = function (comment) {
            comment.addReply(comment.newReply).then(function () {
                comment.newReply = '';
                comment.replying = false;
            }, function () {
                msg.error('Failed to add the reply');
            });
        };

        $scope.cancelReply = function (comment) {
            comment.newReply = '';
            comment.replying = false;
        };
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
    ctrl.IdeaVersionCtrl = ['$scope', '$stateParams',
        function ($scope, $stateParams) {
            $scope.ideaPromise.then(function (idea) {
                $scope.vers = _(idea.versions).find(function (vers) {
                    return $stateParams.versId === vers.unique;
                });
            });
        }];


    return ctrl;
});
