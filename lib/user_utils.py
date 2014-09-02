"""
For Handling user db calls
"""
import json
import datetime

from lib.model import User

from mongoengine import Q

def get_user(user_id):
    my_user = User.objects.get(google_id=user_id)
    user_str = my_user.to_json()
    data = json.loads(user_str)
    return data


def delete_user(token):
    old_user = User.objects.get(google_id=token)
    old_user.delete()
    return old_user

def match_users(search_string):
    list_o_users = User.objects(name__icontains=search_string)[:10]
    data = []
    for people in list_o_users:
        if people.google_id:
            data.append(json.loads(people.to_json()))
    return data

#Return all current app users
def get_all_users():
    data = []
    for users in User.objects:
        if users.google_id:
            data.append(json.loads(users.to_json()))
    return data

def get_list(needed_users):
    data = []
    for a_user in needed_users:
        my_user = User.objects.get(google_id=a_user)
        data.append(json.loads(my_user.to_json()))
    return data
