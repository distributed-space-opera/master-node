# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gateway-comm.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12gateway-comm.proto\x12\x06stream\")\n\x07Request\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"\x19\n\x05Reply\x12\x10\n\x08masterip\x18\x01 \x01(\t2<\n\x0c\x41uthenticate\x12,\n\x08Register\x12\x0f.stream.Request\x1a\r.stream.Reply\"\x00\x42\x16\n\x12org.gateway.protosP\x01\x62\x06proto3')



_REQUEST = DESCRIPTOR.message_types_by_name['Request']
_REPLY = DESCRIPTOR.message_types_by_name['Reply']
Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), {
  'DESCRIPTOR' : _REQUEST,
  '__module__' : 'gateway_comm_pb2'
  # @@protoc_insertion_point(class_scope:stream.Request)
  })
_sym_db.RegisterMessage(Request)

Reply = _reflection.GeneratedProtocolMessageType('Reply', (_message.Message,), {
  'DESCRIPTOR' : _REPLY,
  '__module__' : 'gateway_comm_pb2'
  # @@protoc_insertion_point(class_scope:stream.Reply)
  })
_sym_db.RegisterMessage(Reply)

_AUTHENTICATE = DESCRIPTOR.services_by_name['Authenticate']
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\022org.gateway.protosP\001'
  _REQUEST._serialized_start=30
  _REQUEST._serialized_end=71
  _REPLY._serialized_start=73
  _REPLY._serialized_end=98
  _AUTHENTICATE._serialized_start=100
  _AUTHENTICATE._serialized_end=160
# @@protoc_insertion_point(module_scope)
