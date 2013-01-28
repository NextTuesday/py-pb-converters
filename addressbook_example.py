from addressbook_pb2 import AddressBook
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
            ]
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
adr_book = pbjson.dict2pb(AddressBook, adr_book_json)

#Convert Protobuf to JSoN
new_json = pbjson.pb2json(adr_book)

