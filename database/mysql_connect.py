# encoding=utf-8
import configparser, os, inspect, sys, pymysql
sys.path.append(os.path.abspath(os.getcwd() + '/database'))

# from https://wiki.python.org/moin/ConfigParserExamples
def ConfigSectionMap(section, config):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def connectMysql():
    config = configparser.ConfigParser()
    dbDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    config.read(dbDir + '/config.ini')
    
    ConfigMap = ConfigSectionMap('DB', config)
    mHost = str(ConfigMap['host'])
    mPort = int(ConfigMap['port'])
    mUser = str(ConfigMap['user'])
    mPasswd = str(ConfigMap['passwd'])
    mDb = str(ConfigMap['db'])
    
    conn = pymysql.connect(host = mHost, port = mPort, user = mUser, passwd = mPasswd, db = mDb, charset = 'UTF8')
    return conn
