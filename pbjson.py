#
# Copyright (c) 2013, Next Tuesday GmbH
#       Authored by: Seif Lotfy <sfl@nexttuesday.de>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of the FreeBSD Project.
#

import simplejson
from google.protobuf.descriptor import FieldDescriptor as FD

class ConvertException(Exception):
    pass

def dict2pb(cls, adict, strict=False, extend=None):
    names = []
    extensions = {}
    if extend:
        names = extend.DESCRIPTOR.extensions_by_name.keys()
    for name in names:
        attr = getattr(extend, name)
        if attr.containing_type in extensions: 
          extensions[attr.containing_type].append(attr)
        else: 
          extensions[attr.containing_type]=[attr]

    return dict2pb_(cls, adict, strict, extensions)
    

def dict2pb_(cls, adict, strict=False, extensions={}):
    """
    Takes a class representing the ProtoBuf Message and fills it with data from
    the dict.
    """
    obj = cls()
    for field in obj.DESCRIPTOR.fields:
        if not field.label == field.LABEL_REQUIRED:
            continue
        if not field.has_default_value:
            continue
        if not field.name in adict:
            raise ConvertException('Field "%s" missing from descriptor dictionary.'
                                   % field.name)
    field_names = set([field.name for field in obj.DESCRIPTOR.fields])
    if strict:
        for key in adict.keys():
            if key not in field_names:
                raise ConvertException(
                    'Key "%s" can not be mapped to field in %s class.'
                    % (key, type(obj)))

    if obj.DESCRIPTOR in extensions:
        for field in extensions[obj.DESCRIPTOR]:
            if not field.name in adict or None == adict[field.name]:
                continue
            msg_type = field.message_type
            if field.label == FD.LABEL_REPEATED:
                if field.type == FD.TYPE_MESSAGE:
                    for sub_dict in adict[field.name]:
                        item = getattr(obj, 'Extensions')[field].add()
                        item.CopyFrom(dict2pb_(msg_type._concrete_class, sub_dict, strict, extensions))
                else:
                    map(getattr(obj, 'Extensions')[field].append, adict[field.name])
            else:
                if field.type == FD.TYPE_MESSAGE:
                    value = dict2pb_(msg_type._concrete_class, adict[field.name], strict, extensions)
                    getattr(obj, 'Extensions')[field].CopyFrom(value)
                else:
                    getattr(obj, 'Extensions')[field] = adict[field.name]

    for field in obj.DESCRIPTOR.fields:
        if not field.name in adict:
            continue
        msg_type = field.message_type
        if field.label == FD.LABEL_REPEATED:
            if field.type == FD.TYPE_MESSAGE:
                for sub_dict in adict[field.name]:
                    item = getattr(obj, field.name).add()
                    item.CopyFrom(dict2pb_(msg_type._concrete_class, sub_dict, strict, extensions))
            else:
                map(getattr(obj, field.name).append, adict[field.name])
        else:
            if field.type == FD.TYPE_MESSAGE:
                value = dict2pb_(msg_type._concrete_class, adict[field.name], strict, extensions)
                getattr(obj, field.name).CopyFrom(value)
            else:
                setattr(obj, field.name, adict[field.name])
    return obj


def pb2dict(obj):
    """
    Takes a ProtoBuf Message obj and convertes it to a dict.
    """
    adict = {}
    if not obj.IsInitialized():
        return None
    for field,value in obj.ListFields():
        if field.label == FD.LABEL_REPEATED:
            if field.type == FD.TYPE_MESSAGE:
                if not field.is_extension:
                    adict[field.name] = \
                        [pb2dict(v) for v in getattr(obj, field.name)]
                else:
                    adict[field.name] = \
                        [pb2dict(v) for v in getattr(obj, 'Extensions')[field]]
            else:
                if not field.is_extension:
                    adict[field.name] = [v for v in getattr(obj, field.name)]
                else:
                    adict[field.name] = \
                        [v for v in getattr(obj, 'Extensions')[field]]
        else:
            if field.type == FD.TYPE_MESSAGE:
                if not field.is_extension:
                    adict[field.name] = pb2dict(v)
                else:
                    adict[field.name] = pb2dict(getattr(obj, 'Extensions')[field])
            else:
                if not field.is_extension:
                    adict[field.name] = getattr(obj, field.name)
                else:
                    adict[field.name] = getattr(obj, 'Extensions')[field]

    return adict


def json2pb(cls, json, strict=False):
    """
    Takes a class representing the Protobuf Message and fills it with data from
    the json string.
    """
    return dict2pb(cls, simplejson.loads(json), strict)


def pb2json(obj):
    """
    Takes a ProtoBuf Message obj and convertes it to a json string.
    """
    return simplejson.dumps(pb2dict(obj), sort_keys=True, indent=4)

