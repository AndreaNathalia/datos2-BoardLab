import requests

from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
#-----------------------------------------------------------------------------
#function to add user to list


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

# es.index(index='table', doc_type='link', id='linkhttps', body={'user': 'username'})


#-----------------------------------------------------------------------------

# get all links for tableros
linklist= []
test = es.search(index='table', body={"query": {"match": {'user': 'username'}}})
test2 = test['hits']['hits']
for i in test2:
    linklist.append(i['_id'])
print (linklist)   
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