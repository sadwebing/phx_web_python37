#!/bin/bash
source ~/.bash_profile

basedir=$(cd $(dirname $0); pwd)

function auto_update {
TableName=$1
FileName=$2
md5_now="$TableName:"$(/usr/bin/md5sum ${basedir}/$FileName |awk '{print $1}')

if [ -f ${basedir}/md5_1min.txt ];then
    md5_1min=$(grep $TableName ${basedir}/md5_1min.txt)
else
    md5_1min=$md5_now
    echo "${md5_now}" >> ${basedir}/md5_1min.txt
fi

if [ "${md5_now}" != "${md5_1min}" ];then
    /usr/local/bin/python ${basedir}/update_table.py $TableName
    sed -i '/'$TableName'/ d' ${basedir}/md5_1min.txt
    echo "${md5_now}" >> ${basedir}/md5_1min.txt
fi
}

auto_update tomcat_url tomcat_url.txt
auto_update mail mail.txt
auto_update tomcat_project tomcat_project.txt
