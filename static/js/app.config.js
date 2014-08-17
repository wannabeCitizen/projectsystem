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
            });
    }];
});
