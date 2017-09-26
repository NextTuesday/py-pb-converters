from addressbook_pb2 import AddressBook
import extend_pb2
import pbjson

adr_book_json = {
    "person": [
        {
            "name": "Mohamed Lee",
            "id": 1,
            "phone": [
                {
                "number": "+1234567890",
                "type": 0
                },
                {
                "number": "+2345678901",
                "type": 1
                }
            ],
            "age": 25,
            "sch": [
                {
                "name": "peking university",
                "city": "Beijing"
                },
                {
                "name": "BHSF",
                "city": "Beijing"
                }
            ],
            "used_name":["Tom", "Jerry"],
            "ht": {
                "city":"Shanghai"
            }
        },
        {
        "name": "Ben Bun",
            "id": 2,
            "email": "b@bun.com",
            "phone": [
                {
                "number": "+1234567890",
                "type": 0
                }
            ]
        }
    ]
}

#Convert JSoN to Protobuf
adr_book = pbjson.dict2pb(AddressBook, adr_book_json, extend=extend_pb2)
#print adr_book
import simplejson as json
print json.dumps(adr_book_json, indent=4)

#Convert Protobuf to JSoN
new_json = pbjson.pb2json(adr_book)
print new_json


