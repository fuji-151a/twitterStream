#! /bin/bash
PROPFILE=$1
DATE=`date +"%Y%m%d"`
OUTPUTFILE=tweet${DATE}.json
#ERRORLOG=tweet${DATE}.log
if [ ! -e ${OUTPUTFILE} ]; then
    touch ${OUTPUTFILE}
    echo [ >> ${OUTPUTFILE}
fi
CMD="python tweetStream.py ${PROPFILE} ${OUTPUTFILE}"
${CMD}
echo -e "\n]" >> ${OUTPUTFILE}
