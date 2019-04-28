import re
import configparser
import os
import json
import datetime
from lib.DB import MySQL
_dir = os.path.abspath(os.path.dirname(__file__))

def Time():
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + datetime.datetime.now().strftime('.%f')[:4]
    return date

class LoadConfig(object):
    scale = os.getenv('SCALE') or 'dev'
    #scale = 'online'
    _conffile = os.path.join(_dir, scale, 'config.ini')
    cf = configparser.ConfigParser()
    cf.read(_conffile)

class GetConfigure(object):
    '''
    解析配置文件
    '''

    @staticmethod
    def get_mysql_client():
        host = LoadConfig.cf.get('mysql', 'host')
        port = LoadConfig.cf.get('mysql', 'port')
        user = LoadConfig.cf.get('mysql', 'user')
        passwd = LoadConfig.cf.get('mysql', 'passwd')
        db = LoadConfig.cf.get('mysql', 'database')
        #
        client = MySQL(host=host, port=port, user=user, passwd=passwd, db=db)
        return client

    @staticmethod
    def get_serverlist():
        config_files = os.path.join(_dir, LoadConfig.scale, 'serverlist.json')
        # serverlist = json.load(open(config_files, 'r'))
        with open(config_files) as f:
            s = ''
            for i in f.readlines():
                s += re.sub(r'(^//.*"?$)|(^/\*(.*?)\*/$)', '', i)
                # s += i.strip('\n')
            serverlist = json.loads(s)
            #serverlist = s

        return serverlist

    @staticmethod
    def get_docker_image(server_name):
        image = LoadConfig.cf.get('docker_image', server_name)
        return image