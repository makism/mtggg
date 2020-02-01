 ￼
#!/usr/bin/env bash

export LOG_FILE="/home/vagrant/bootstrap.sh.log"

sudo chown -R vagrant /home/vagrant
sudo chgrp -R vagrant /home/vagrant


sudo apt-get update
sudo apt-get upgrade
