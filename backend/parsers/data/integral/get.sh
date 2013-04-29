#!/bin/sh

COUNT=10
MAX=1287

while [ ${COUNT} -le ${MAX} ] 
do
  NUM=`echo ${COUNT} | awk '{printf("%04d",$1)}'`
  echo "${NUM}"

  #Search on Count
  [ ! -s "${NUM}.csv" ] && curl --silent "http://integral.esac.esa.int/isocweb/schedule.html?action=schedule&startRevno=${COUNT}&endRevno=${COUNT}&reverseSort=&format=csv"  | grep -v "^\"Rev"> ${NUM}.csv
  COUNT=`expr ${COUNT} + 1`
done

exit 0
