__author__ = 'karisu'
import redis
redis_con = redis.Redis('localhost')


filename = 'results.out'
f = open(filename, "r")
text = f.readline()
while text :
    #print text
    text_split = text.split()
    redis_con.zadd('userHistogramm', text_split[0], text_split[1] )

    text = f.readline()







