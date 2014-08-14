#!/bin/bash

echo Provisioning system...

echo Installing prereq packages...
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y python-pip mongodb

pip install Flask Flask-Restful Flask-Login Flask_Googlelogin mongoengine bson

python /vagrant/manager.py &

echo "Provisioning completed"
