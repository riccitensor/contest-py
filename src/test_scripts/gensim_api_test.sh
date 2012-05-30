#!/bin/sh

#export server_url=http://localhost:5002
readonly server_url=http://localhost:5002
# readonly server_url=http://178.63.4.204:5001

echo

echo "testing the whole workflow of initiation of the training set until querying"

#curl $server_url/test/hello_world

#curl --data "id=1905&text=This a for post parameters Test" $server_url/test/http_param_ext

# python -m gensim.test.run_simserver /tmp/ramdisk/linguisticModel/test5 &
# python2.7 -m gensim.test.run_simserver /tmp/test5 &



# create a new training set
# return 1 for success, -1 for error/database exists
curl --data "training_id=5" $server_url/unsupervised/clustering/gensim/initTrainingSet

# fill up the training set /unsupervised/clustering/gensim/fillTrainingSet
# return if successful "fill ok\n"
curl --data "document_text=küche&document_id=doc17&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=straße&document_id=doc18&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=Eins Minus (-) Zwei&document_id=doc19&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet


curl --data "document_text=Human machine interface for lab abc computer applications&document_id=doc11&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=A survey of user opinion of computer system response time&document_id=doc12&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=The EPS user interface management system&document_id=doc13&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=System and human system engineering testing of EPS&document_id=doc3&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=Relation of user perceived response time to error measurement&document_id=doc2&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=The generation of random binary unordered trees&document_id=doc1&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet

curl --data "document_text=The intersection graph of paths in trees&document_id=doc1&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=Graph minors IV Widths of trees and well quasi ordering&document_id=doc1&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=Graph minors A survey&document_id=doc1&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet

curl --data "document_text=Kate Winslet was first considered for and reportedly offered the role of Helena Ravenclaw. The role was rejected by her agent before she was able to consider it, believing that Winslet would not want to follow suit with every other actor in Britain by being a part of Harry Potter. The role subsequently went to Kelly Macdonald&document_id=doc105&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=Incorrectly regarded as goofs: When Harry reveals himself to Snape in the Great Hall he is wearing a Hogwarts robe. However his regular clothes are beneath the robe, and he is seen tossing it to the side once Snape flees&document_id=doc104&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=It was reported that a huge blaze wrecked the Hogwarts set after a battle scene went spectacularly wrong. According to the report, explosives used in action sequences set light to scenery for the wizardry school, and that firefighters battled for 40 minutes to bring the flames under control but the set - centerpiece for the film's Battle of Hogwarts climax - was left badly damaged. It was later confirmed that the fire was greatly exaggerated, and that the set that had been damaged was going to need be rebuilt anyway for use in another scene. Some actors were still filming at the studio but none of the movie's biggest stars - Daniel Radcliffe (Harry), Emma Watson (Hermione) or Rupert Grint (Ron Weasley) - were involved. No one was injured. See more » &document_id=doc103&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=The final chapter begins as Harry, Ron, and Hermione continue their quest of finding and destroying the Dark Lord's three remaining Horcruxes, the magical items responsible for his immortality. But as the mystical Deathly Hallows are uncovered, and Voldemort finds out about their mission, the biggest battle begins and life as they know it will never be the same again.&document_id=doc102&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet
curl --data "document_text=Browse the most recent weekly U.S. box office summary, and find links to the top box office performers, top rentals, and much more -- including lists of the best (and worst) movies in all categories, voted on by our users.&document_id=doc101&training_id=5" $server_url/unsupervised/clustering/gensim/fillTrainingSet


# train the set with the filled documents
# return if successful: "training ok\n"
curl --data "training_id=5" $server_url/unsupervised/clustering/gensim/trainTrainingSet

# fill the indexing set
# return if successfuk: "fill ok\n"
curl --data "document_text=Graph minors A survey&document_id=doc1&training_id=5" $server_url/unsupervised/clustering/gensim/fillIndexingSet
curl --data "document_text=Relation of user perceived response time to error measurement&document_id=doc2&training_id=5" $server_url/unsupervised/clustering/gensim/fillIndexingSet
curl --data "document_text=Relation of user perceived greatest movies and their memories&document_id=doc3&training_id=5" $server_url/unsupervised/clustering/gensim/fillIndexingSet
curl --data "document_text=Graph minors A survey&document_id=doc3&training_id=5" $server_url/unsupervised/clustering/gensim/fillIndexingSet

curl --data "document_text=Graph minors And a survey monkey&document_id=doc4&training_id=5" $server_url/unsupervised/clustering/gensim/fillIndexingSet
curl --data "document_text=Hello Hello, lets go into the movies&document_id=doc5&training_id=5" $server_url/unsupervised/clustering/gensim/fillIndexingSet
curl --data "document_text=üüü Relation of user perceived response time with the constraint of errorless measurement&document_id=doc6&training_id=5" $server_url/unsupervised/clustering/gensim/fillIndexingSet

curl --data "document_text=monkey island is a nice game&document_id=doc14&training_id=5" $server_url/unsupervised/clustering/gensim/fillIndexingSet
curl --data "document_text=lets watch all the harry potter movies&document_id=doc15&training_id=5" $server_url/unsupervised/clustering/gensim/fillIndexingSet
curl --data "document_text=emma watson won't film any movies soon because her relation to university...&document_id=doc16&training_id=5" $server_url/unsupervised/clustering/gensim/fillIndexingSet


# index the filled data
# return if successful: "indexing ok\n"
curl --data "training_id=5" $server_url/unsupervised/clustering/gensim/indexSet

#curl --data "training_id=5" $server_url/unsupervised/clustering/gensim/deleteTrainingSet
#curl --data "training_id=5" $server_url/unsupervised/clustering/gensim/deleteIndexSet

# query for documents
# return json if successful with a list of similar items including the one queried
curl --data "training_id=5&document_id=doc2" $server_url/unsupervised/clustering/gensim/queryById
curl --data "training_id=5&document_id=doc4" $server_url/unsupervised/clustering/gensim/queryById


