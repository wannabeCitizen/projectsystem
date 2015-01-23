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
            .state('orgs.new', {
                url: '/new',
                templateUrl: 'static/template/editOrg.html',
                controller: 'NewOrgCtrl'
            })
            .state('org', {
                url: '/org/:orgId',
                templateUrl: 'static/template/org.html'
            })
            .state('org.edit', {
                url: '/edit',
                templateUrl: 'static/template/editOrg.html',
                controller: 'EditOrgCtrl'
            })
            .state('org.newIdea', {
                url: '/idea/new',
                templateUrl: 'static/template/editIdea.html',
                controller: 'NewIdeaCtrl'
            })
            .state('org.idea', {
                url: '/idea/:ideaId',
                templateUrl: 'static/template/idea.html'
            })
            .state('org.idea.edit', {
                url: '/edit',
                templateUrl: 'static/template/editIdea.html',
                controller: 'EditIdeaCtrl'
            })
            .state('org.idea.newVersion', {
                url: '/version/new',
                views: {
                    'inner': {
                        templateUrl: 'static/template/editIdeaVers.html',
                        controller: 'NewIdeaVersCtrl'
                    }
                }
            })
            .state('org.idea.version', {
                url: '/version/:versId',
                views: {
                    'inner': {
                        templateUrl: 'static/template/ideaVers.html'
                    }
                }
            })
            .state('org.idea.version.edit', {
                url: '/edit',
                templateUrl: 'static/template/editIdeaVers.html',
                controller: 'EditIdeaVersCtrl'
            })
            .state('project', {
                url:'/project',
                templateUrl: 'static/template/project.html'
            });
    }];
});
