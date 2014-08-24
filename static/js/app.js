/*jslint browser:true */
/*global define */

// Create the main application module
define([
    'angular',

    // app components
    'app.config',
    'app.directive',
    'app.svc',
    'app.ctrl',
    'app.templates',
    'org.ctrl',
    'org.svc',

    // angular modules
    'angular-ui-router',
    'angular-resource',
    'google-plus-signin'
], function (angular, appConfig, appDir, appSvc, appCtrl, appTemplates, orgCtrl, orgSvc) {
    'use strict';

    return angular.module('MainAppModule', ['ui.router', 'ngResource', 'directive.g+signin'])
        .config(appConfig)
        .directive(appDir)
        .factory(appSvc)
        .controller(appCtrl)
        .run(appTemplates)
        .controller(orgCtrl)
        .factory(orgSvc);
});