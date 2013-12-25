#! /bin/bash
PROPFILE=$1
RUNTODAY=`date +"%d"`
while true
do
DATE=`date +"%Y%m%d%H%M"`
OUTPUTFILE=tweet${DATE}.json
#ERRORLOG=tweet${DATE}.log
if [ ! -e ${OUTPUTFILE} ]; then
    touch ${OUTPUTFILE}
    echo [ >> ${OUTPUTFILE}
fi
CMD="python tweetStream.py ${PROPFILE} ${OUTPUTFILE}"
${CMD}
echo -e "\n]" >> ${OUTPUTFILE}
TODAY=`date +"%d"`
if ![ ${TODAY} -eq ${RUNTODAY} ]; then
    echo "BASH END"
    break;
fi
done
