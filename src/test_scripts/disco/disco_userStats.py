__author__ = 'karisu'


from disco.core import Job, result_iterator
import disco


def map(line, params):
    #print line
    mytuple = line.split(',')
    #print mytuple

    #for word in line.split():
    #    yield word, 1
    yield mytuple[0], 1
    yield 'itemid', 1




def reduce(iter, params):
    from disco.util import kvgroup
    for word, counts in kvgroup(sorted(iter)):
        yield word, sum(counts)


if __name__ == '__main__':


    job = Job().run(input=["tag://data:contesthundred"],
    #job = Job().run(input=["tag://data:contestall"],
                    map=map,
                    map_reader = disco.worker.classic.func.chain_reader,
                    reduce=reduce)

    for word, count in result_iterator(job.wait(show=True)):

        print word, count
