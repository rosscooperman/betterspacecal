#!/bin/sh
export PATH=/usr/local/bin:$PATH
(
cd $HOME
#git clone git://github.com/rosscooperman/betterspacecal.git
cd $HOME/betterspacecal
git pull
bundle
rake assets:precompile
sudo /opt/nginx/sbin/nginx -s reload

) >> /tmp/release.log 2>&1 
exit 0
