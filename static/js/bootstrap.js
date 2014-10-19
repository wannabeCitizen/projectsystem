/*jslint browser:true */
/*global requirejs */

// define the dependencies with requirejs
requirejs.config({
    // baseUrl is implicitly relative to this file
    waitSeconds: 0,

    paths: {
        jquery: "../lib/jquery/jquery",
        angular: "../lib/angular/angular",
        'angular-animate': "../lib/angular-animate/angular-animate",
        'angular-sanitize': "../lib/angular-sanitize/angular-sanitize",
        'angular-resource': "../lib/angular-resource/angular-resource",
        'angular-ui-router': "../lib/angular-ui-router/angular-ui-router",
        'angular-strap': "../lib/angular-strap/angular-strap.min",
        'angular-strap-tpl': "../lib/angular-strap/angular-strap.tpl.min",
        marked: "../lib/marked/marked",
        fastclick: "../lib/fastclick/fastclick",
        moment: "../lib/moment/moment",
        underscore: "../lib/underscore/underscore",
        css: "../lib/require-css/css",
        less: "../lib/require-less/less",
        lessc: "../lib/require-less/lessc",
        normalize: "../lib/require-less/normalize",
        gapi: "../lib/gapi/index",
        'google-plus-signin': "../lib/angular-directive.g-signin/google-plus-signin",
        toaster: "../lib/AngularJS-Toaster/toaster"
    },

    shim: {
        angular: {
            deps: ['jquery'],
            exports: 'angular'
        },
        gapi: {
            exports: 'gapi'
        },
        'angular-animate': ['angular'],
        'angular-sanitize': ['angular'],
        'angular-resource': ['angular'],
        'angular-strap': ['angular', 'angular-animate'],
        'angular-strap-tpl': ['angular', 'angular-animate', 'angular-strap'],
        'angular-ui-router': ['angular'],
        'google-plus-signin': ['angular'],
        toaster: ['angular', 'angular-animate']
    },

    less: {
        relativeUrls: true
    }
});

// This is the main application entry point, invoked by requirejs
// bootstraps the angularjs app with the dom
requirejs([
    'angular',
    'app',
    'fastclick',
    'less!../less/main'
],
    function (angular, app, fastclick) {
        'use strict';

        angular.element().ready(function () {
            angular.bootstrap(document, [app.name]);
            fastclick.attach(document.body);
        });
    });
