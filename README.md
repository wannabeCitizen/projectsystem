Democratic Project Manager
=============

This will be a web app used for collectives of people to manage democratically controlled projects.

Getting Started
---------------
#### Building the Code
All of the code for the front-end web app is tested, compiled, and minified using the Grunt build system. All 3rd party dependencies are managed using NPM and Bower.

##### Set up your development environment
You only have to follow these steps once, to get all of the build tools on your dev machine

1. Download and install [nodejs](http://nodejs.org/)
2. Use NPM (from nodejs) to install [Bower](http://bower.io/), [Grunt](http://gruntjs.com/), and [Karma](http://karma-runner.github.io/)

  ```
  npm install -g bower
  npm install -g grunt-cli
  npm install -g karma
  ```
3. Pull down the build dependencies using NPM

  ```
  cd /path/to/project/root
  npm install
  ```

##### Build
Whenever the source code changes, it must be rebuilt before it will run in production.
```
cd /path/to/project/root
grunt
```

#### Test Environment
You can use Vagrant to set up a completely isolated development and test environment on any PC.

1. Install [VirtualBox](http://virtualbox.org)
2. Install [Vagrant](http://vagrantup.com)
3. From the project folder, start vagrant
  
  ```
  vagrant up
  ```
4. Edit the `hosts` file on your system (required for authentication to work). The vm uses a bridged adapter, so you need to find its ip address on your network, and add an entry like the following:

 ```
 192.168.0.123 projects.d0ck.me
 ```
4. In your browser, navigate to http://projects.d0ck.me/dev
5. Any changes to the source will be immediately reflected after a browser refresh
6. To run the compiled, production code instead, navigate to http://projects.d0ck.me/
