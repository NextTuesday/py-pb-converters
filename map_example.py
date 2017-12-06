import pbjson
import map_pb2

d = {'d':{1:{'id':1, 'name':'hello'}, 2:{'id':2, 'name':'world'}}}

m = pbjson.dict2pb(map_pb2.M, d)
print m
