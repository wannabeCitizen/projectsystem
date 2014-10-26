/*jslint browser:true */
/*global define */

define(['angular', 'gapi'], function (angular, gapi) {
    'use strict';

    var factory = {};

    factory.UserSvc = ['$q', '$rootScope', '$log', '$http', 'UserApi', function ($q, $rootScope, $log, $http, UserApi) {
        var svc = {};
        svc.currentUser = {};
        $rootScope.currentUser = svc.currentUser;

        svc.usersEqual = function (u1, u2) {
            return u1 && u2 && (u1.google_id === u2.google_id);
        };

        svc.isCurrentUser = function (u) {
            return svc.usersEqual(u, svc.currentUser);
        };

        svc.isCurrentUserId = function (id) {
            return svc.currentUser.google_id === id;
        };

        svc.getList = function (idList) {
            return UserApi.getList(idList).$promise;
        };

        svc.getById = function (id) {
            return UserApi.get({userId: id}).$promise;
        };

        $rootScope.$on('event:google-plus-signin-success', function (event, authResult) {
            // Send login to server or save into cookie
            $log.log('user authenticated with google', authResult);
            angular.copy({}, svc.currentUser);
            svc.currentUser.googleAuth = authResult;

            var plus = $q.defer();
            gapi.client.load('plus', 'v1', function () {
                gapi.client.plus.people.get({userId: 'me'}).execute(function (resp) {
                    return resp.error ? plus.reject(resp.error) : plus.resolve(resp);
                });
            });

            plus.promise.then(function (plusData) {
                svc.currentUser.googlePlus = plusData;

                return $http.post('/api/login', svc.currentUser).then(function (response) {
                    return response.data;
                });
            }).then(function (apiUser) {
                svc.currentUser.api = apiUser;
                svc.currentUser.loggedIn = true;

                svc.currentUser.name = (svc.currentUser.googlePlus && svc.currentUser.googlePlus.displayName) ||
                    (svc.currentUser.googleAuth && svc.currentUser.googleAuth.name) ||
                    (svc.currentUser.api && svc.currentUser.api.name);

                svc.currentUser.imageUrl = svc.currentUser.googlePlus && svc.currentUser.googlePlus.image && svc.currentUser.googlePlus.image.url;

                svc.currentUser.id = svc.currentUser.google_id = (svc.currentUser.googlePlus && svc.currentUser.googlePlus.id) ||
                    (svc.currentUser.api && svc.currentUser.api.google_id);

                svc.currentUser.logout = function () {
                    gapi.auth.signOut();
                };
            }, function (err) {
                $log.error('login failed', err);
                gapi.auth.signOut();
            });
        });

        $rootScope.$on('event:google-plus-signin-failure', function (event, authResult) {
            // Auth failure or signout detected
            $log.log('user logout or auth error', authResult);
            $http.get('/api/logout');
            angular.copy({}, svc.currentUser);
        });

        return svc;
    }];

    return factory;
});
