/*jshint unused: vars */
/*global define, describe, beforeEach, afterEach, it, expect*/

define(['angular', 'angular-mocks', 'app'], function (angular, mocks, app) {
    'use strict';

    describe('Controller: P1Ctrl', function () {
        var $scope, P1Ctrl;

        beforeEach(mocks.module(app.name));
        beforeEach(mocks.inject(function ($injector, $rootScope) {
            // The $controller service is used to create instances of controllers
            var $controller = $injector.get('$controller');

            $scope = $rootScope.$new();
            P1Ctrl = $controller('P1Ctrl', { $scope: $scope });
        }));

        it('should attach to the scope', function () {
            expect($scope.data).toBe('Check out this data binding!');
        });
    });
});
