#!/bin/sh
#
# Daily Cron script
#
(
cd $HOME/betterspacecal/backend/parsers
python fermi.py
python herschel.py
python integral.py
python nustar.py
python suzaku.py
python swift.py
python xmm-newton.py
cd ..
python image-grabber.py
) >> /tmp/daily.txt 2>&1

