#!/bin/sh
#
# Daily Cron script
#
(
cd $HOME/betterspacecal/backend
python fermi.py
python herschel.py
python integral.py
python nustar.py
python suzaku.py
python swift.py
python xmm-newton.py
) >> /tmp/daily.txt 2>&1
