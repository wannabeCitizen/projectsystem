/*jslint browser:true */
/*global define */

// This is the main angularjs module configuration
define([], function () {
    'use strict';
    return ['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise("/");

        $stateProvider
            .state('home', {
                url: '/',
                templateUrl: 'static/template/home.html'
            })
            .state('orgs', {
                url: '/org',
                templateUrl: 'static/template/orgs.html'
            })
            .state('newOrg', {
                url: '/org/new',
                templateUrl: 'static/template/newOrg.html'
            })
            .state('org', {
                url: '/org/:id',
                templateUrl: 'static/template/org.html'
            });
    }];
});
