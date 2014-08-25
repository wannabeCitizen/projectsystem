/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var factory = {};

    factory.MsgSvc = ['$timeout', '$log', 'toaster',
        function ($timeout, $log, toaster) {
            var svc = {};

            svc.success = function (title, body) {
                $log.log.apply(this, arguments);
                toaster.pop('success', title, body);
            };

            svc.error = function (title, body) {
                $log.error.apply(this, arguments);
                toaster.pop('error', title, body);
            };

            svc.warning = function (title, body) {
                $log.warn.apply(this, arguments);
                toaster.pop('warning', title, body);
            };

            svc.info = function (title, body) {
                $log.info.apply(this, arguments);
                toaster.pop('info', title, body);
            };

            svc.debug = function () {
                $log.debug.apply(this, arguments);
            };

            svc.clear = toaster.clear;

            return svc;
        }];

    return factory;
});
