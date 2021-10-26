import requests
import memcache
from elasticsearch import Elasticsearch
# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


mc = memcache.Client(['127.0.0.1:11211'], debug=0)
mc.set("some_key", "Some value")
value = mc.get("some_key")
mc.set("another_key", 3)
mc.delete("another_key")
mc.set("key", "1")   # note that the key used for incr/decr must be a string.
mc.incr("key")
mc.decr("key")

#-----------------------------------------------------------------------------
#function to add user to list
print(value)

# es.index(index='users', doc_type='people', id=username, body={'email':email,'password':password})


#-----------------------------------------------------------------------------

#function to check password

# test = es.search(index='users', body={"query": {"match": {'_id': username}}})
# test2 = test['hits']['hits']

# for i in test2:
#     userpass = i['_source']['password']
#     if userpass == password:
#         userpass2 = userpass
# if userpass2 == password:        
#     return render_template('index.html', username = username)


#-----------------------------------------------------------------------------

# function to create link in tablero

# es.index(index='table', doc_type='link', id=username, body={'link': link})


#-----------------------------------------------------------------------------

# get all links for tableros
# linklist= []
# test = es.search(index='table', body={"query": {"match": {'user': username}}})
# test2 = test['hits']['hits']
# for i in test2:
#     linklist.append(i['source']['link'])
# print (linklist)   
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------





# try:    
#     test =es.get(index='users', doc_type='people', id='username')
#     print(test)
# except:
#     print('not')

#index some test data
# es.index(index='test-index', doc_type='test', id=1, body={'test': 'test'})
# es.delete(index='test-index', doc_type='test', id=1)


# print(test)
# es.index(index='test-index', doc_type='test', id=1, body={'test': 'test'})