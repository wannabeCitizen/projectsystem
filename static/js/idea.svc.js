/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore'], function (angular, _) {
    'use strict';

    var factory = {};

    factory.Idea = [function () {
        // This is a class ctor
        return function (resource) {
            var idea = angular.extend(this, resource);
        };
    }];

    factory.IdeaSvc = ['Idea', 'IdeaApi', function (Idea, IdeaApi) {
        var svc = {};

        svc.getById = function (orgId, ideaId) {
            return IdeaApi.get({orgId: orgId, ideaId: ideaId}).$promise.then(function (idea) {
                return new Idea(idea);
            });
        };

        return svc;
    }];

    return factory;
});
