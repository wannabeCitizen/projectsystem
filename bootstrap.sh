#!/bin/bash
echo Provisioning system...
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y python-pip mongodb python-software-properties python-dev build-essential git

pip install Flask Flask-Restful Flask-Login Flask_Googlelogin mongoengine bson

# apt-add-repository -y ppa:chris-lea/node.js
# apt-get update
# apt-get install -y nodejs

# npm install -g bower
# npm install -g grunt-cli
# npm install -g karma

# cd /vagrant
# npm install --no-bin-links
# bower --allow-root -y install

python /vagrant/manager.py &

echo "Provisioning completed. Point your browser to http://localhost:55555/"
