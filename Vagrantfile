# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/trusty64"

    # accessing "localhost:80" will access port 5000 on the guest machine.
    # config.vm.network :forwarded_port, guest: 80, host: 80

    # bridge adapter
    config.vm.network :public_network

    # Run provisioning scripts
    config.vm.provision :shell, :path => "bootstrap.sh"
end
