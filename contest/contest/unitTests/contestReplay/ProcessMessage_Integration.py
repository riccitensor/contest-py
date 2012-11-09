import _mysql
import json
import time
import redis
from contest.config import config_local
from contest.controller.ProcessMessage import ProcessMessage

__author__ = 'karisu'



class ProcessMessage_Integration(object):

    recommendable_items = []
    item_domain_relation = {}

    def __init__(self):
        """ construct """
        pass
        # TODO create an error logger which is searchable. In best case a raw text log which will be search by hadoop...


    def random_impression(self):
        """ """
        mysql_host = config_local.mysql_host
        user = config_local.mysql_user
        password = config_local.mysql_password
        db = _mysql.connect(host=mysql_host, user=user, passwd=password, db="db_youfilter")
        sql = """SELECT json FROM contest_messages c WHERE id > 100000 AND type = 'impression' LIMIT 100000"""
        db.query(sql)

        r = db.use_result()
        return r


    def random_clickfeedback(self):

        mysql_host = config_local.mysql_host
        user = config_local.mysql_user
        password = config_local.mysql_password
        db = _mysql.connect(host=mysql_host, user=user,
                            passwd=password, db="db_youfilter")

        sql = """SELECT userid, itemid, src, date as timestamp FROM db_youfilter.clickfeedback c \
                WHERE 1 LIMIT 1000"""

        db.query(sql)
        r = db.use_result()
        result = r.fetch_row(maxrows=n_maxrows) # fetch N row maximum

        replay_time = time2.time()
        n = 1
        print "import data"

    def throw_against_message_processor(self, request = 10000.0, mod = 1000):
        result_length_error = 0.0
        right_domain_error = 0.0
        none_error = 0.0
        recommendable_error = 0.0

        request_amount = 0
        result_counter = 0
        sql = self.random_impression()
        result = sql.fetch_row(maxrows=int(request)) # fetch N row maximum
        for message in result:
            result_counter += 1
            message = message[0]
            pM = ProcessMessage(message)

            decoded_message = json.loads(message)
            #print "Message: {}".format(message)
            if "config" in decoded_message and \
               "recommend" in decoded_message["config"] and \
               decoded_message["config"]["recommend"] == True:
                result_length_error += self.check_for_result_length(pM.results, decoded_message)

                right_domain_error_tmp, none_error_tmp = self.check_for_right_domain(pM.results, decoded_message)
                right_domain_error += right_domain_error_tmp
                none_error += none_error_tmp

                #recommendable_error += self.check_for_recommendable()

                if result_counter % mod == 0:
                    request_amount += mod
                    print "impression count:{}".format(request_amount)
                    print "result Length error quota:\t{}%".format(100 * result_length_error/request_amount)
                    print "right domain error quota:\t{}%".format(100 * right_domain_error/request_amount)
                    print "none error quota:\t{}%".format(100 * none_error/request_amount)

                    print ""

                    #print "right_domain_error: {}".format(right_domain_error)
                    #print "none_error: {}".format(none_error)
        #print "error count:{}".format(result_length_error)




    def check_for_result_length(self, results, decoded_message):
        if decoded_message["id"] > 10200:
            pass
        actual_result_length = len(results)
        desired_result_length = decoded_message["config"]["limit"]

        if actual_result_length != desired_result_length:
            return 1
        else:
            return 0

    def add_to_domain_association(self, decoded_message):
        try:
            if int(decoded_message["domain"]["id"]) not in self.item_domain_relation:
                self.item_domain_relation[int(decoded_message["domain"]["id"])] = [int(decoded_message["item"]["id"])]
            elif int(decoded_message["item"]["id"]) not in self.item_domain_relation[int(decoded_message["domain"]["id"])]:
                self.item_domain_relation[int(decoded_message["domain"]["id"])].append(int(decoded_message["item"]["id"]))
        except:
            # TODO add some error message to the log files here
            pass




    def check_for_right_domain(self, results, decoded_message):
        self.add_to_domain_association(decoded_message)
        """ check if the items in results are from the right domain """
        wrong_domain_errors = 0
        none_errors = 0
        domain_id = int(decoded_message["domain"]["id"])
        for i in results:
            if i == 'None':
                none_errors += 1
            elif int(i) not in self.item_domain_relation[domain_id]:
                wrong_domain_errors += 1

        #print decoded_message
        #print results
        return wrong_domain_errors, none_errors

    def check_for_recommendable(self, results, decoded_message):
        pass


if __name__ == "__main__":
    redis.Redis("localhost")
    redis_con = redis.Redis("localhost")
    redis_con.flushall()
    print "test"
    pMI = ProcessMessage_Integration()
    print "first round of impressions"
    pMI.throw_against_message_processor()
#    print "second round of impressions"
#    pMI.throw_against_message_processor()