import riak

client = riak.RiakClient()
user_bucket = client.bucket('user')

# We're creating the user data & keying off their username.
new_user = user_bucket.new('johndoe', data={
    'first_name': 'John',
    'last_name': 'Doe',
    'gender': 'm',
    'website': 'http://example.com/',
    'is_active': True,
})
# Note that the user hasn't been stored in Riak yet.
new_user.store()



import riak

client = riak.RiakClient()
user_bucket = client.bucket('user')

johndoe = user_bucket.get('johndoe')

# You've now got a ``RiakObject``. To get at the values in a dictionary
# form, call:
johndoe_dict = johndoe.get_data()

#print johndoe_dict



import riak

client = riak.RiakClient()
# First, you need to ``add`` the bucket you want to MapReduce on.
query = client.add('user')
# Then, you supply a Javascript map function as the code to be executed.
query.map("""function(v) { var data = JSON.parse(v.values[0].data); 
if(data.is_active == true) { return [[v.key, data]]; } return []; }""")

for result in query.run():
    # Print the key (``v.key``) and the value for that key (``data``).
    print "%s - %s" % (result[0], result[1])

# Results in something like:
#
# mr_smith - {'first_name': 'Mister', 'last_name': 'Smith', 'is_active': True}
# johndoe - {'first_name': 'John', 'last_name': 'Doe', 'is_active': True}
# annabody - {'first_name': 'Anna', 'last_name': 'Body', 'is_active': True}