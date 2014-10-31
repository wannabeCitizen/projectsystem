from flask import request, jsonify

from flask.ext import restful
from flask.ext.restful import abort
from flask_login import current_user

from lib.verify import is_owner, can_add
from lib.org_utils import (get_org, get_all_orgs, delete_org, create_org, 
                          update_org, add_member, remove_member, remove_owner,
                          add_owner, match_orgs)

import uuid
import json


class OrganizationEP(restful.Resource):

    url =  '/api/org/<string:org_id>'

    def get(self, org_id):
        return get_org(org_id)

    def delete(self, org_id):
        verify = is_owner(org_id, current_user.google_id)
        if verify is True:
            delete_org(org_id)
            return "Success"
        else:
            return abort(401, message="User is not an owner")

    def put(self, org_id):
        new_data = request.get_json()
        verify = is_owner(org_id, current_user.google_id)
        if verify is True:
            return update_org(org_id, **new_data)
        else:
            return abort(401, message="User is not an owner")

class AllOrgs(restful.Resource):

    url = '/api/org'

    def get(self):
        if 'search' in request.args and request.args['search'] != None:
            search = request.args['search']
            ten_orgs = match_orgs(search)
            return ten_orgs
        elif request.args:
            abort(400, message="Bad Pe-ram-it-ers")
        else:
            return get_all_orgs()

    def post(self):
        new_org_data = request.get_json()
        new_org_data['unique'] = str(uuid.uuid4())
        return create_org(current_user.google_id, **new_org_data)

class OrgMember(restful.Resource):

    url = '/api/org/<string:org_id>/member/<string:user_id>'

    def put(self, org_id):
        user_id = request.get_json()['google_id']
        verify = can_add(org_id, current_user.google_id)
        if verify is True:
            new_member = add_member(org_id, user_id)
            return "Success"
        else:
            return abort(401, message="User is not an owner")

    def delete(self, org_id, user_id):
        verify = is_owner(org_id, current_user.google_id)
        if verify is True:
            old_member = remove_member(org_id, user_id)
            return "Success"
        else: 
            return abort(401, message="User is not an owner")

class OrgOwner(restful.Resource):

    url = '/api/org/<string:org_id>/owner/<string:user_id>'

    def put(self, org_id):
        user_id = request.get_json()['google_id']
        verify = can_add(org_id, current_user.google_id)
        if verify is True:
            new_owner = add_owner(org_id, user_id)
            return "Success"
        else:
            return abort(401, message="User is not an owner")

    def delete(self, org_id, user_id):
        verify = is_owner(org_id, current_user.google_id)
        if verify is True:
            old_owner = remove_owner(org_id, user_id)
            return "Success"
        else: 
            return abort(401, message="User is not an owner")


