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
                templateUrl: 'static/template/editOrg.html',
                controller: 'NewOrgCtrl'
            })
            .state('org', {
                url: '/org/:orgId',
                templateUrl: 'static/template/org.html'
            })
            .state('editOrg', {
                url: '/org/:orgId/edit',
                templateUrl: 'static/template/editOrg.html',
                controller: 'EditOrgCtrl'
            })
            .state('newIdea', {
                url: '/org/:orgId/idea/new',
                templateUrl: 'static/template/editIdea.html',
                controller: 'NewIdeaCtrl'
            })
            .state('idea', {
                url: '/org/:orgId/idea/:ideaId',
                templateUrl: 'static/template/idea.html'
            })
            .state('editIdea', {
                url: '/org/:orgId/idea/:ideaId/edit',
                templateUrl: 'static/template/editIdea.html',
                controller: 'EditIdeaCtrl'
            });
    }];
});
