/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var ctrl = {};

    ctrl.BaseCtrl = ['$scope', 'MessageSvc', function ($scope, msg) {
        $scope.msg = msg;
    }];

    ctrl.P1Ctrl = ['$scope', function ($scope) {
        $scope.data = 'Check out this data binding!';
    }];

    return ctrl;
});
