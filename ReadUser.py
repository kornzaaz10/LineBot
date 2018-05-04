import firebase_admin
from firebase_admin import (
    credentials, db
)
import json

cred = credentials.Certificate('service_account.json')
default_app = firebase_admin.initialize_app(cred,
{
    'databaseURL': 'https://myproject-4c93f.firebaseio.com/'
})

print('Default App:',default_app)
ref = db.reference('/customers')
for c in ref.get():
    print(type(c))
    obj = ref.child(c)
    print(c)
    print('\t',obj.child('id').get())
    print('\t',obj.child('name').get())
# print(ref.get())