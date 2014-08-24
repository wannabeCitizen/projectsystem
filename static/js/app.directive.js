/*jslint browser:true */
/*global define */

define(['marked'], function (marked) {
    'use strict';

    var dir = {};

    dir.psNavbar = [function () {
        return {
            restrict: 'E',
            templateUrl: 'static/template/navbar.html'
        };
    }];

    dir.marked = [function () {
        return {
            restrict: 'AE',
            replace: true,
            scope: {
                opts: '=',
                marked: '='
            },
            link: function (scope, element, attrs) {
                var set = function (val) {
                    element.html(marked(val || '', scope.opts || null));
                };

                set(scope.marked || element.text() || '');

                if (attrs.marked) {
                    scope.$watch('marked', set);
                }
            }
        };
    }];

    return dir;
});
