#!/bin/sh


WEEK="700"
while [ $WEEK -le 831 ]
do
  OUTPUT="rxte.${WEEK}.txt"
  echo "Checking ${OUTPUT}"
  [ ! -f "${OUTPUT}" ] && curl --silent http://heasarc.gsfc.nasa.gov/docs/xte/SOF/sts/Wk${WEEK}.txt > ${OUTPUT}
  WEEK=`expr ${WEEK} + 1`
done

cat *.txt | awk -f rxte.awk > rxte.txt
