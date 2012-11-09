'''
Created on 04.12.2011

config file which holds local changeable configuration data like server names, ports etc

@author: christian.winkelmann@plista.com

'''

config_redis_server_basic = "localhost"
config_rabbitmq_server = "localhost"

cassandra_hosts = ['46.51.176.41', 'localhost'] # this is for pooling, but its not implemented in python cql and I am too lazy to do that myself

cassandra_host = 'localhost'
cassandra_port = 9160

messaging_debug = True # use this to circumvent the messaging system

mysql_host = "localhost"
mysql_user = 'root'
mysql_password = 'kar--32!'

team_id = 22
api_version = 1.0
