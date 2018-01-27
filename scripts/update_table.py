#!/usr//bin/env python
#-_- coding:utf-8 -_-
import os,sys,logging,datetime
import django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "monitor.settings")
django.setup()
from check_tomcat.models import tomcat_project, tomcat_url, mail
from monitor.settings import DATABASES as databases

#获取当前目录
current_dir = os.path.abspath(os.path.dirname(__file__))
#print basedir

cursor = django.db.connection.cursor()

tomcat_info_list = []
tomcat_project_list = []
mail_list = []
def get_list(filename, list_name):
    with open('%s/%s' %(current_dir,filename)) as f:
        lines = f.readlines()
    for line in lines:
        if line == '\n' or '#' in line:
            continue
        else:
            #print line.split('|')
            list_name.append(line.replace('\n', '').split('|'))

def backup_table(table_name):
    backup_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    os.system('mysql -h%s -u%s -p%s -e "select * from %s.%s" > %s/backup/%s.txt.%s ' 
            %(databases['default']['HOST'], databases['default']['USER'], databases['default']['PASSWORD'], databases['default']['NAME'], table_name, current_dir, table_name, backup_time))

def update_tomcat_project():
    get_list('tomcat_project.txt', tomcat_project_list)
    backup_table('check_tomcat_tomcat_project')
    info_list = tomcat_project.objects.all()
    for info in info_list:
        info.delete()
    cursor.execute('alter table check_tomcat_tomcat_project AUTO_INCREMENT=1; ')
    for tomcat_info in tomcat_project_list:
        if len(tomcat_info) != 8:
            continue
        else:
            info = tomcat_project(product=tomcat_info[0], project=tomcat_info[1], code_dir=tomcat_info[2], tomcat=tomcat_info[3], main_port=tomcat_info[4], script=tomcat_info[5], jdk=tomcat_info[6], status=tomcat_info[7])
            info.save()

def update_tomcat_url():
    get_list('tomcat_url.txt', tomcat_info_list)
    backup_table('check_tomcat_tomcat_url')
    info_list = tomcat_url.objects.all()
    for info in info_list:
        info.delete()
    cursor.execute('alter table check_tomcat_tomcat_url AUTO_INCREMENT=1; ')
    for url_info in tomcat_info_list:
        if len(url_info) != 3:
            continue
        else:
            info = tomcat_url(project=url_info[1], url=url_info[0],domain=url_info[2])
            info.save()

def update_mail():
    get_list('mail.txt', mail_list)
    backup_table('check_tomcat_mail')
    #os.system('mysql -h192.168.100.164 -umonitor -pag866.com -e "select * from monitor.check_tomcat_mail" > %s/backup/mail.txt.%s ' %(current_dir, backup_time))
    #cursor.execute('select * from check_tomcat_mail into outfile "%s/backup/mail.txt.%s" '%(current_dir, backup_time))
    info_list = mail.objects.all()
    for info in info_list:
        info.delete()
    cursor.execute('alter table check_tomcat_mail AUTO_INCREMENT=1; ')
    for mail_info in mail_list:
        if len(mail_info) != 4:
            continue
        else:
            info = mail(name=mail_info[0], mail_address=mail_info[1], status=mail_info[2], role=mail_info[3])
            info.save()

if __name__ == '__main__':
    if not os.path.isdir('%s/backup' %current_dir):
        os.mkdir('%s/backup' %current_dir)
    if len(sys.argv) == 1:
        logging.error('No table specified.')
    elif sys.argv[1] == 'tomcat_url':
        logging.info('update table tomcat_url.')
        update_tomcat_url()
    elif sys.argv[1] == 'mail':
        logging.info('update table mail.')
        update_mail()
    elif sys.argv[1] == 'tomcat_project':
        logging.info('update table tomcat_project.')
        update_tomcat_project()
    else:
        logging.error('talbe %s doesn\'t exit.' %sys.argv[0])
