/*jslint browser:true */
/*global define */

define(['marked', 'gapi'], function (marked, gapi) {
    'use strict';

    var dir = {};

    dir.psNavbar = ['$http', '$rootScope', '$log', function ($http, $rootScope, $log) {
        return {
            restrict: 'E',
            templateUrl: 'static/template/dir/navbar.html',
            scope: true,
            link: function (scope) {
                $rootScope.$on('event:google-plus-signin-success', function (event, authResult) {
                    // Send login to server or save into cookie
                    $log.log('user authenticated', authResult);
                    $rootScope.googleAuth = authResult;
                    $http.post('/api/login', authResult).then(function (response) {
                        $log.log('login api success', response.data);
                        $rootScope.currentUser = response.data;
                    }, function (err) {
                        $log.error('login api fail', err);
                        $rootScope.currentUser = null;
                    });

                    gapi.client.load('plus', 'v1', function () {
                        var request = gapi.client.plus.people.get({
                            'userId': 'me'
                        });
                        request.execute(function (resp) {
                            $log.log('google plus api', resp);
                            $rootScope.googlePlus = resp;
                            $rootScope.$digest();
                        });
                    });
                });
                $rootScope.$on('event:google-plus-signin-failure', function (event, authResult) {
                    // Auth failure or signout detected
                    $log.log('user logout or auth error', authResult);
                    $rootScope.googleAuth = authResult;
                    $rootScope.currentUser = null;
                    $rootScope.googlePlus = null;
                });

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

    return dir;
});
