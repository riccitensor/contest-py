This is the Python Component to the Plista Contest.
See www.plista.com and contest.plista.com

This Component or Service consists of two parts
1. The webserver
1.1. Architecture 
The webserver is Flask. See http://flask.pocoo.org/ for details. The minimal effort to setup flask and to provide a RESTful Interface to native Python functions are the reason to use it.  
1.2. Installation

$ sudo apt-get install python-dev python-pip python-virtualenv redis-server ipython python-nose gfortran python-dev libatlas3gf-base libblas-dev libatlas-base-dev liblapack3gf gfortran gfortran-multilib g++  libatlas3gf-base 

now goto the folder where the python code should be located later/already is. It should be a safe and nice location, since the webserver is integrated nothing more will be needed so far.
Either checkout or create the python environment variable folder

$ cd/mkdir python_env
$ cd python_env
$ virtualenv env
and now you have to source the environment
$ . env/bin/activate

Install the other packages
sudo pip install Flask numpy scipy scikit-learn neurolab sqlitedict Pyro4
#sudo pip install -U scikit-learn
#sudo pip install -U neurolab


1.3. Run the Server with
$ python FlaskServer.py 
it will output:  
* Running on http://127.0.0.1:5000/
* Restarting with reloader
it won't output anything more


turn your browser to 
http://127.0.0.1:5000/test_hello_world
Or do a 
$ curl http://127.0.0.1:5000/test_hello_world
And you will see a friendly "hello world"

2. The Python Algorithm

To run this some more packages are needed
remember to be in your virtual environment because later we need to upgrade numpy and scipy

cd clickabilly_gensim
$ . env/bin/activate
$ 
$ sudo pip install numpy 
$ python -Wd -c 'import numpy; numpy.test()'
$ python -Wd -c 'import scipy ; scipy.test() '
$ sudo pip install scipy
$ sudo easy_install sqlitedict
$ sudo easy_install Pyro4

$ sudo pip install --upgrade gensim


At first stance the algorithm will be based on LSI or Latent Sementic Indexing provide by the python package
gensim
http://groups.google.com/group/gensim/browse_thread/thread/2dfce414b79cd81d
to checkout the current alpha version


See for details on using our implemenation 
http://nlp.fi.muni.cz/projekty/gensim/simserver.html


ATTENTION: 
When the server was restarted then you have to restart the FLASK webserver and first SOURCE the Folder with "$ . env/bin/activate " 









