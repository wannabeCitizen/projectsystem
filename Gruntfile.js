/*jslint node:true */
module.exports = function (grunt) {
    'use strict';

    require('load-grunt-tasks')(grunt);

    var saveFileWithHeader = function (path, text, banner) {
        grunt.file.write(path, grunt.template.process(banner) + text);
    };

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        banner: '/*! <%= pkg.name %> v<%= pkg.version %> | (c) <%= grunt.template.today("yyyy") %> | built on <%= grunt.template.today("yyyy-mm-dd") %> */\n',

        // download external deps
        bower: {
            install: {
                options: {
                    targetDir: './static/lib',
                    layout: 'byComponent',
                    cleanTargetDir: true
                }
            }
        },

        // Dependency management and minification
        requirejs: {
            app: {
                options: {
                    name: "almond",
                    optimize: 'none',
                    optimizeCss: "standard",
                    inlineText: true,
                    include: ['bootstrap'],
                    stubModules: ['css'],
                    preserveLicenseComments: false,
                    baseUrl: "static/js/",
                    siteRoot: "./",
                    mainConfigFile: "static/js/bootstrap.js",
                    paths: {
                        'css-builder': "../lib/require-css/css-builder",
                        'less-builder': "../lib/require-less/less-builder",
                        almond: "../lib/almond/almond",
                        'app.templates': 'empty:'
                    },
                    exclude: ['normalize'],
                    out: function (text) {
                        saveFileWithHeader("static/js/dist/app.js", text, "<%= banner %>");
                    }
                }
            }
        },

        // inline angular templates
        ngtemplates: {
            options: {
                htmlmin: {
                    collapseWhitespace: true,
                    removeComments: true
                },
                bootstrap: function (module, script) {
                    return "define('app.templates', [], function() { return ['$templateCache', function ($templateCache) {" + script + "}]; });";
                }
            },
            app: {
                src: 'static/template/**/*.html',
                cwd: './',
                dest: 'static/js/dist/app.js',
                options: { append: true }
            },
            test: {
                src: 'static/template/**/*.html',
                cwd: './',
                dest: 'test/app.templates.js'
            }
        },

        uglify: {
            options: {
                preserveComments: false,
                report: "gzip",
                banner: "<%= banner %>"
            },
            app: {
                files: {
                    'static/js/dist/app.min.js': ['static/js/dist/app.js']
                }
            }
        },

        processhtml: {
            app: {
                files: {
                    'templates/index.html': 'templates/devIndex.html'
                }
            }
        },

        // JSLint style enforcer
        jslint: {
            app: {
                src: ['static/js/*.js'],
                directives: {
                    browser: true,
                    vars: true,
                    regexp: true,
                    unparam: true,
                    predef: ['define', 'require', 'requirejs']
                },
                options: {
                    junit: 'reports/jslint-app.xml'
                }
            }
        },

        // Karma test runner
        karma: {
            app: {
                options: {

                    // base path that will be used to resolve all patterns (eg. files, exclude)
                    basePath: '',

                    // available frameworks: https://npmjs.org/browse/keyword/karma-adapter
                    frameworks: ['jasmine', 'requirejs'],

                    // list of files / patterns to load in the browser
                    files: [
                        'test/test-main.js',
                        {pattern: 'test/**/*.js', included: false},
                        {pattern: 'static/js/**/*', included: false},
                        {pattern: 'static/less/**/*', included: false},
                        {pattern: 'static/lib/**/*', included: false}
                    ],

                    // available reporters: https://npmjs.org/browse/keyword/karma-reporter
                    reporters: ['dots', 'junit'],
                    junitReporter: {
                        outputFile: 'reports/karma-results.xml'
                    },

                    // web server port
                    port: 9876,

                    // enable / disable colors in the output (reporters and logs)
                    colors: true,

                    logLevel: 'INFO',

                    // enable / disable watching file and executing tests whenever any file changes
                    autoWatch: false,

                    // available browser launchers: https://npmjs.org/browse/keyword/karma-launcher
                    browsers: [
                        'Chrome',
                        'Firefox',
                        'PhantomJS'
                    ],

                    // Continuous Integration mode
                    // if true, Karma captures browsers, runs the tests and exits
                    singleRun: true
                }
            }
        },

        // Test web server
        connect: {
            dev: {
                options: {
                    port: 9000,
                    debug: true,
                    keepalive: true,
                    open: 'http://localhost:9000/src/'
                }
            },
            dist: {
                options: {
                    port: 9001,
                    base: 'dist',
                    keepalive: true,
                    open: 'http://localhost:9001/'
                }
            }
        }
    });

    // Default task(s).
    grunt.registerTask('deps', ['npm-install', 'bower']);
    grunt.registerTask('test', ['deps', 'jslint', 'ngtemplates:test', 'karma']);
    grunt.registerTask('build', ['deps', 'requirejs', 'ngtemplates:app', 'uglify', 'processhtml']);
    grunt.registerTask('default', ['test', 'build']);
};
