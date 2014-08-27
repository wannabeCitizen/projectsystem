/*jslint browser:true */
/*global define */

define(['marked', 'gapi'], function (marked, gapi) {
    'use strict';

    var dir = {};

    dir.psNavbar = ['UserSvc', function (UserSvc) {
        return {
            restrict: 'E',
            templateUrl: 'static/template/dir/navbar.html',
            scope: true,
            link: function (scope) {
                scope.userDrop = [
                    {
                        "text": "Logout",
                        "click": "logout()"
                    }
                ];

                scope.logout = function () {
                    gapi.auth.signOut();
                };
            }
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

    dir.formValidStyle = [function () {
        return {
            restrict: 'A',
            require: '^form',
            link: function (scope, element, attrs, formCtrl) {
                var name = attrs.formValidStyle;

                var updateClass = function () {
                    var formElem = formCtrl[name];
                    if (!formElem || !formElem.$dirty) { return; }

                    if (formElem.$valid) {
                        element.addClass('has-success');
                        element.removeClass('has-error');
                    } else {
                        element.removeClass('has-success');
                        element.addClass('has-error');
                    }
                };

                scope.$watch(function () { return formCtrl[name] && formCtrl[name].$dirty; }, updateClass);
                scope.$watch(function () { return formCtrl[name] && formCtrl[name].$valid; }, updateClass);
            }
        };
    }];

    dir.collapseBtn = [function () {
        return {
            restrict: 'E',
            template: '<i class="fa" ng-class="icon()"></i>',
            scope: {
                collapsed: '='
            },
            link: function (scope, element) {
                scope.icon = function () {
                    return {
                        'fa-angle-double-right': scope.collapsed,
                        'fa-angle-double-down': !scope.collapsed
                    };
                };

                element.on('click', function () {
                    scope.collapsed = !scope.collapsed;
                    scope.$apply();
                });
            }
        };
    }];

    return dir;
});
