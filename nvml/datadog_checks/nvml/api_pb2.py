# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: api.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 5, 27, 2, '', 'api.proto')
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\tapi.proto\x12\x08v1alpha1\"\x19\n\x17ListPodResourcesRequest\"I\n\x18ListPodResourcesResponse\x12-\n\rpod_resources\x18\x01 \x03(\x0b\x32\x16.v1alpha1.PodResources\"a\n\x0cPodResources\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x11\n\tnamespace\x18\x02 \x01(\t\x12\x30\n\ncontainers\x18\x03 \x03(\x0b\x32\x1c.v1alpha1.ContainerResources\"O\n\x12\x43ontainerResources\x12\x0c\n\x04name\x18\x01 \x01(\t\x12+\n\x07\x64\x65vices\x18\x02 \x03(\x0b\x32\x1a.v1alpha1.ContainerDevices\"=\n\x10\x43ontainerDevices\x12\x15\n\rresource_name\x18\x01 \x01(\t\x12\x12\n\ndevice_ids\x18\x02 \x03(\t2e\n\x12PodResourcesLister\x12O\n\x04List\x12!.v1alpha1.ListPodResourcesRequest\x1a\".v1alpha1.ListPodResourcesResponse\"\x00\x62\x06proto3'  # noqa: E501
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'api_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_LISTPODRESOURCESREQUEST']._serialized_start = 23
    _globals['_LISTPODRESOURCESREQUEST']._serialized_end = 48
    _globals['_LISTPODRESOURCESRESPONSE']._serialized_start = 50
    _globals['_LISTPODRESOURCESRESPONSE']._serialized_end = 123
    _globals['_PODRESOURCES']._serialized_start = 125
    _globals['_PODRESOURCES']._serialized_end = 222
    _globals['_CONTAINERRESOURCES']._serialized_start = 224
    _globals['_CONTAINERRESOURCES']._serialized_end = 303
    _globals['_CONTAINERDEVICES']._serialized_start = 305
    _globals['_CONTAINERDEVICES']._serialized_end = 366
    _globals['_PODRESOURCESLISTER']._serialized_start = 368
    _globals['_PODRESOURCESLISTER']._serialized_end = 469
# @@protoc_insertion_point(module_scope)
