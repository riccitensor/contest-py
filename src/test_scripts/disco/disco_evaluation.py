__author__ = 'karisu'


from disco.core import Job, result_iterator
import disco

def map(line, params):
    for word in line.split():
        yield word, 1




def reduce(iter, params):
    from disco.util import kvgroup
    for word, counts in kvgroup(sorted(iter)):
        yield word, sum(counts)

# , and add map_reader = disco.worker.classic.func.chain_reader

#job = Job().run(input=["http://discoproject.org/media/text/chekhov.txt"],
if __name__ == '__main__':


    job = Job().run(input=["tag://data:bigtxt"],
                    map=map,
                    map_reader = disco.worker.classic.func.chain_reader,
                    reduce=reduce)
    for word, count in result_iterator(job.wait(show=True)):
        print word, count
