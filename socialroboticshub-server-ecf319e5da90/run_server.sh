#!/bin/bash
export VAGRANT_HOME=.vagrant
vagrant halt
vagrant plugin install vagrant-vbguest
vagrant up --provision
read -p "Press any key to stop the server..."
vagrant halt
