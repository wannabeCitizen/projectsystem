/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var ctrl = {};

    ctrl.BaseCtrl = ['$scope',
        function ($scope) {
            $scope.test = 'it works';
        }];

    return ctrl;
});
