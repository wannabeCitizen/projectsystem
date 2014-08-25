from flask import request, jsonify

from flask.ext import restful
from flask.ext.restful import abort
from flask_login import current_user

from lib.db_utils import (get_org, get_all_orgs, delete_org, create_org,
                      update_org)
from lib.verify import is_owner, can_add

import uuid
import json


class OrganizationEP(restful.Resource):
    def get(self, org_id):
        organization = get_org(org_id)
        return organization

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
            organization = update_org(org_id, **new_data)
            return organization
        else:
            return abort(401, message="User is not an owner")

class AllOrgs(restful.Resource):
    def get(self):
        if request.args['search']:
            ten_orgs = match_orgs(search)
            return ten_orgs
        else:
            all_orgs = get_all_orgs()
            return all_orgs

    def post(self):
        new_org_data = request.get_json()
        #Eventuall will need to add an owner below
        # user = get_user(my_args.owner)
        new_org_data['unique'] = str(uuid.uuid4())
        organization = create_org(current_user.google_id, **new_org_data)
        return json.loads(organization.to_json())


class OrgMember(restful.Resource):
    def put(self, org_id):
        user_id = request.get_json()['google_id']
        verify = can_add(org_id, current_user.google_id)
        if verify is True:
            new_member = add_member(org_id, user_id)
            return "Success"
        else:
            return abort(401, message="User is not an owner")

    def delete(self, org_id):
        user_id = request.get_json()['google_id']
        verify = is_owner(org_id, current_user.google_id)
        if verify is True:
            old_member = remove_member(org_id, user_id)
            return "Success"
        else: 
            return abort(401, message="User is not an owner")

class OrgOwner(restful.Resource):
    def put(self, org_id):
        user_id = request.get_json()['google_id']
        verify = can_add(org_id, current_user.google_id)
        if verify is True:
            new_owner = add_owner(org_id, user_id)
            return "Success"
        else:
            return abort(401, message="User is not an owner")

    def delete(self, org_id):
        user_id = request.get_json()['google_id']
        verify = is_owner(org_id, current_user.google_id)
        if verify is True:
            old_owner = remove_owner(org_id, user_id)
            return "Success"
        else: 
            return abort(401, message="User is not an owner")


