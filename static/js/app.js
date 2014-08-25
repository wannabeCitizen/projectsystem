/*jslint browser:true */
/*global define */

// Create the main application module
define([
    'angular',

    // app components
    'app.config',
    'app.dir',
    'app.svc',
    'app.ctrl',
    'app.templates',
    'org.ctrl',
    'org.svc',
    'user.svc',
    'user.dir',

    // angular modules
    'angular-ui-router',
    'angular-resource',
    'google-plus-signin',
    'angular-strap-tpl',
    'angular-animate',
    'toaster'
], function (angular, appConfig, appDir, appSvc, appCtrl, appTemplates, orgCtrl, orgSvc, userSvc, userDir) {
    'use strict';

    return angular.module('MainAppModule', ['ui.router', 'ngResource', 'directive.g+signin', 'mgcrea.ngStrap', 'ngAnimate', 'toaster'])
        .config(appConfig)
        .directive(appDir)
        .factory(appSvc)
        .controller(appCtrl)
        .run(appTemplates)
        .controller(orgCtrl)
        .factory(orgSvc)
        .factory(userSvc)
        .directive(userDir);
});
