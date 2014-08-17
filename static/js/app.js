/*jslint browser:true */
/*global define */

// Create the main application module
define(['angular', 'app.config', 'app.directive', 'app.svc', 'app.ctrl', 'app.templates', 'angular-ui-router'], function (angular, appConfig, appDir, appSvc, appCtrl, appTemplates) {
    'use strict';

    return angular.module('MainAppModule', ['ui.router'])
        .config(appConfig)
        .directive(appDir)
        .factory(appSvc)
        .controller(appCtrl)
        .run(appTemplates);
});
