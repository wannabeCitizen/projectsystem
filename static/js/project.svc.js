/*jslint browser:true, nomen:true */
/*global define */

define(['angular', 'underscore', 'moment'], function (angular, _, moment) {
	'use strict';

	var factory = {};

	factory.Project = ['$http', '$resource', 'UserSvc', function ($http, $resource, UserSvc, Version) {
		
		var Project = function (resource) {
			angular.extend(this, resource);
			
			this.orgId = this.my_org && this.my_org.unique;
			this.projectId = this.unique;
			this.url = '/api/org' + this.orgId + '/project/' + this.projectId;

			_(this.comments).each(function(){

			});

			_(this.votes).each(function (){

			});

			this.serialize = function() {
				return _(this).pick('title', 'unique', 'short_description', 'based_on', 'budget', 'quorum', 'majority', 'text', 'complete')
			}

			this.save = function() {
				return $http.put(this.url, this.serialize()).then(
					angular.bind(this.function(response){
						angular.extend(this, response.data);
						return this;
					})
				);
			};

			this.userIsFollowing = function (){
				return _(this.followers).find(function (follower) {
					return UserSvc.isCurrentUserId(follower);
				});
			};

			this.follow = function () {
				return this.$follow().then(angular.bind(this, function () {
					this.followers.push(UserSvc.currentUser.id);
					return this;
				}));
			};

			this.unfollow = function () {
				return this.$unfollow().then(angular.bind(this, function () {
					this.followers = _(this.followers).without(UserSvc.currentUser.id);
					return this;
				}));
			};
			//Will further need methods for members, votes, roles
			//phases, tasks, revisions, and comments

		};
		//Need to add Project.api
		//Need to add Project.getbyId


	}]

})