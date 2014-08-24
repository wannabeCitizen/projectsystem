/*jslint browser:true */
/*global define */

define(['marked', 'gapi'], function (marked, gapi) {
    'use strict';

    var dir = {};

    dir.psNavbar = ['$http', 'MessageSvc', function ($http, msg) {
        return {
            restrict: 'E',
            templateUrl: 'static/template/navbar.html',
            scope: true,
            link: function (scope) {
                scope.$on('event:google-plus-signin-success', function (event, authResult) {
                    // Send login to server or save into cookie
                    msg.success('Login worked!');
                    msg.success(authResult);
                    scope.googleAuth = authResult;
                    $http.post('/api/login', authResult).then(function (response) {
                        msg.success('login api success: ' + response.data);
                    }, function (err) {
                        msg.error('login api fail: ' + err);
                    });
                });
                scope.$on('event:google-plus-signin-failure', function (event, authResult) {
                    // Auth failure or signout detected
                    msg.error('Sign-in state: ' + authResult.error);
                    scope.googleAuth = authResult;
                });

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

    return dir;
});
