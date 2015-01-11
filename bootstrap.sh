#!/bin/bash
echo Provisioning system...
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y python-pip mongodb python-software-properties python-dev build-essential git

apt-add-repository -y ppa:chris-lea/node.js
apt-get update
apt-get install -y nodejs

npm install -g bower
npm install -g grunt-cli
# npm install -g karma

cd /vagrant
pip install -r requirements.txt
npm install --no-bin-links

grunt build

python /vagrant/manager.py &

echo "Provisioning completed. Point your browser to http://127.0.0.1:80/"
