/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var dir = {};

    dir.psNavbar = [function () {
        return {
            restrict: 'E',
            templateUrl: 'static/template/navbar.html'
        };
    }];

    return dir;
});
