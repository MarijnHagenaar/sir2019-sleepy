@echo off
SET VAGRANT_HOME=.vagrant
vagrant halt
vagrant plugin install vagrant-vbguest
vagrant up --provision
echo Press any key to stop the server...
pause>nul
vagrant halt
