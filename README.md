py-pb-converters
================

py-pb-converters is a set of python convinience scripts for conversion between
Google's Protocol Buffers and JSoN.

* Free software: BSD licensed
* Python 2.6+
* Source code and issue tracker: https://github.com/NextTuesday/py-pb-converters


----------------
Example of usage:

from addressbook_pb2 import AddressBook
import pbjson

# Convert python dict to Protobuf
adr_book = pbjson.dict2pb(AddressBook, adr_book_json)

# Convert Protobuf to JSoN
new_json = pbjson.pb2json(adr_book)
