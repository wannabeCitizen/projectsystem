/*jslint browser:true */
/*global define */

define([], function () {
    'use strict';

    var factory = {};

    factory.MessageService = ['$timeout', function ($timeout) {
        var svc = {
            autoDismiss: 5000,
            messages: []
        };

        svc.add = function (err, txt) {
            var msg = {
                error: err,
                txt: txt,
                dismissed: false
            };
            svc.messages.push(msg);

            if (svc.autoDismiss) {
                $timeout(function () {
                    msg.dismissed = true;
                }, svc.autoDismiss);
            }
        };

        svc.error = function (txt) {
            svc.add(true, txt);
        };

        svc.success = function (txt) {
            svc.add(false, txt);
        };

        svc.clear = function () {
            svc.messages.length = 0;
        };

        svc.last = function () {
            if (svc.messages.length === 0) { return false; }

            var msg = svc.messages[svc.messages.length - 1];
            return msg.dismissed ? false : msg;
        };

        return svc;
    }];

    return factory;
});
