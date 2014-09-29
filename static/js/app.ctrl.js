/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var ctrl = {};

    ctrl.BaseCtrl = ['$scope', 'UserSvc',
        function ($scope, UserSvc) {
            $scope.test = 'it works';
        }];

    return ctrl;
});
