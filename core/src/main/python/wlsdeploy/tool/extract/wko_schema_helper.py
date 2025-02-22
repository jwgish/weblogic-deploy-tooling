"""
Copyright (c) 2020, 2022, Oracle and/or its affiliates.
Licensed under the Universal Permissive License v 1.0 as shown at https://oss.oracle.com/licenses/upl.
"""
from oracle.weblogic.deploy.util import FileUtils

from wlsdeploy.exception import exception_helper
from wlsdeploy.exception.expection_types import ExceptionType
from wlsdeploy.json.json_translator import JsonStreamToPython
from wlsdeploy.logging import platform_logger
from wlsdeploy.util import dictionary_utils

DOMAIN_RESOURCE_SCHEMA_ROOT = "openAPIV3Schema"
DOMAIN_RESOURCE_SCHEMA_FILE = 'domain-crd-schema-v8.json'
DOMAIN_RESOURCE_SCHEMA_PATH = 'oracle/weblogic/deploy/wko/' + DOMAIN_RESOURCE_SCHEMA_FILE

SIMPLE_TYPES = [
    'integer',
    'number',
    'string',
    'boolean'
]

OBJECT_TYPES = [
    'object',
    None
]

UNSUPPORTED_FOLDERS = [
    'status',
    'metadata/initializers',
    'metadata/ownerReferences'
]

# some object list members don't use 'name' as a key
OBJECT_NAME_ATTRIBUTES = {
    'spec/adminServer/adminService/channels': 'channelName',
    'spec/clusters': 'clusterName',
    'spec/managedServers': 'serverName'
}

_logger = platform_logger.PlatformLogger('wlsdeploy.deploy')
_class_name = 'wko_schema_helper'


def get_domain_resource_schema(exception_type=ExceptionType.DEPLOY):
    """
    Read the WKO domain resource schema from its resource path.
    """
    _method_name = 'get_domain_resource_schema'

    template_stream = None
    try:
        template_stream = FileUtils.getResourceAsStream(DOMAIN_RESOURCE_SCHEMA_PATH)
        if template_stream is None:
            ex = exception_helper.create_exception(exception_type, 'WLSDPLY-10010', DOMAIN_RESOURCE_SCHEMA_PATH)
            _logger.throwing(ex, class_name=_class_name, method_name=_method_name)
            raise ex

        full_schema = JsonStreamToPython(DOMAIN_RESOURCE_SCHEMA_FILE, template_stream, True).parse()

        # remove the root element, since it has a version-specific name
        schema = full_schema[DOMAIN_RESOURCE_SCHEMA_ROOT]

    finally:
        if template_stream:
            template_stream.close()

    return schema


def is_single_object(schema_map):
    """
    Return True if the schema map describes a single object.
    :param schema_map: the schema map to be examined
    :return: True if the map identifies a single object
    """
    property_type = get_type(schema_map)
    if property_type in OBJECT_TYPES:
        return get_map_element_type(schema_map) is None
    return False


def is_object_array(schema_map):
    """
    Return True if the schema map describes an object array.
    :param schema_map: the schema map to be examined
    :return: True if the map identifies an object array
    """
    property_type = get_type(schema_map)
    if property_type == "array":
        return get_array_element_type(schema_map) in OBJECT_TYPES
    return False


def is_object_type(schema_map):
    """
    Return True if the schema map describes an object or object array.
    :param schema_map: the schema map to be examined
    :return: True if the map identifies an object or object array
    """
    return is_single_object(schema_map) or is_object_array(schema_map)


def is_simple_map(schema_map):
    """
    Return True if the schema map describes a simple map.
    :param schema_map: the schema map to be examined
    :return: True if the map identifies a simple map
    """
    property_type = get_type(schema_map)
    if property_type in OBJECT_TYPES:
        return get_map_element_type(schema_map) is not None
    return False


def is_simple_array(schema_map):
    """
    Return True if the schema map describes a simple array.
    :param schema_map: the schema map to be examined
    :return: True if the map identifies a simple array
    """
    property_type = get_type(schema_map)
    if property_type == "array":
        return get_array_element_type(schema_map) not in OBJECT_TYPES
    return False


def is_simple_type(schema_map):
    """
    Return True if the schema map describes a simple type.
    :param schema_map: the schema map to be examined
    :return: True if the map identifies a simple type
    """
    property_type = get_type(schema_map)
    return property_type in SIMPLE_TYPES


def get_array_element_type(schema_map):
    item_info = get_array_item_info(schema_map)
    return get_type(item_info)


def get_map_element_type(schema_map):
    additional = dictionary_utils.get_dictionary_element(schema_map, "additionalProperties")
    return get_type(additional)


def get_array_item_info(schema_map):
    return dictionary_utils.get_dictionary_element(schema_map, "items")


def get_properties(schema_map):
    properties = dictionary_utils.get_element(schema_map, "properties")
    return properties or {}


def get_type(schema_map):
    return dictionary_utils.get_element(schema_map, "type")


def get_enum_values(schema_map):
    return dictionary_utils.get_element(schema_map, 'enum')


def is_unsupported_folder(path):
    return path in UNSUPPORTED_FOLDERS


def get_object_list_key(schema_path):
    """
    Return the name of the attribute that acts as a key for objects in an object list.
    In most cases, this is 'name', but there are a few exceptions.
    :param schema_path: the path to be checked
    :return: the object key
    """
    mapped_key = dictionary_utils.get_element(OBJECT_NAME_ATTRIBUTES, schema_path)
    if mapped_key is not None:
        return mapped_key
    return 'name'


def append_path(path, element):
    if path:
        return path + "/" + element
    return element
