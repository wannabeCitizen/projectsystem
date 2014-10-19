/*jslint browser: true, nomen: true */
(function (requirejs) {
    'use strict';

    var allTestFiles = [],
        pathToModule = function (path) {
            return path.replace(/^\/base\//, '../../').replace(/\.js$/, '');
        };

    Object.keys(window.__karma__.files).forEach(function (file) {
        if (/^\/base\/test\/.*(spec|test)\.js$/i.test(file) || /^\/base\/test\/helpers\/.*\.js$/i.test(file)) {
            // Normalize paths to RequireJS module names.
            allTestFiles.push(pathToModule(file));
        }
    });

    requirejs.config({
        // Karma serves files under /base, which is the basePath from your config file
        baseUrl: '/base/static/js',
        waitSeconds: 0,

        paths: {
            'app.templates': "/base/test/app.templates",
            jquery: "/base/static/lib/jquery/jquery",
            angular: "/base/static/lib/angular/angular",
            'angular-mocks': "/base/static/lib/angular-mocks/angular-mocks",
            'angular-animate': "/base/static/lib/angular-animate/angular-animate",
            'angular-sanitize': "/base/static/lib/angular-sanitize/angular-sanitize",
            'angular-resource': "/base/static/lib/angular-resource/angular-resource",
            'angular-ui-router': "/base/static/lib/angular-ui-router/angular-ui-router",
            'angular-strap': "/base/static/lib/angular-strap/angular-strap.min",
            'angular-strap-tpl': "/base/static/lib/angular-strap/angular-strap.tpl.min",
            marked: "/base/static/lib/marked/marked",
            fastclick: "/base/static/lib/fastclick/fastclick",
            moment: "/base/static/lib/moment/moment",
            underscore: "/base/static/lib/underscore/underscore",
            css: "/base/static/lib/require-css/css",
            gapi: "/base/static/lib/gapi/index",
            'google-plus-signin': "../lib/angular-directive.g-signin/google-plus-signin",
            toaster: "/base/static/lib/AngularJS-Toaster/toaster"
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
            'angular-mocks': {
                deps: ['angular'],
                exports: 'angular.mock'
            },
            'angular-strap': ['angular', 'angular-animate'],
            'angular-strap-tpl': ['angular', 'angular-animate', 'angular-strap'],
            'angular-ui-router': ['angular'],
            'google-plus-signin': ['angular'],
            toaster: ['angular', 'angular-animate']
        },

        // dynamically load all test files
        deps: allTestFiles,

        // we have to kickoff jasmine, as it is asynchronous
        callback: window.__karma__.start
    });
}(window.requirejs));
