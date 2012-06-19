__author__ = 'karisu'

from disco.core import result_iterator
import disco



if __name__ == "__main__":
    from mymodule import FirstJob
    from mymodule import SecondJob


    #last = FirstJob().run(input=["tag://data:contest20"],
    last = FirstJob().run(input=["tag://data:contesthundred"],
    #last = FirstJob().run(input=["tag://data:implicit_all"],
                          map_reader = disco.worker.classic.func.chain_reader
    ).wait(show=False)

    for word, count in result_iterator(last):
        print word, count

    print "done with first stage"

    next = SecondJob().run(input=last).wait(show=False)

    for word, count in result_iterator(next):
        print word, count

    print "done with second stage"