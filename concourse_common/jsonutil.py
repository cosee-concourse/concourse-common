import json
import sys
import tempfile

from concourse_common import common
from concourse_common.request import Request
from jsonschema import Draft4Validator


def load_payload():
    payload = json.load(sys.stdin)
    _, folder_name = tempfile.mkstemp()
    common.log_info("Logging payload to {}".format(folder_name))
    with open(folder_name, 'w') as fp:
        fp.write(json.dumps(payload))
    return payload


def load_and_validate_payload(schemas, request):
    payload = load_payload()
    if request == Request.CHECK:
        schema = schemas.check_schema
    elif request == Request.IN:
        schema = schemas.in_schema
    else:
        schema = schemas.out_schema
    valid = validate_json(payload, schema)
    if valid:
        return valid, payload
    else:
        return valid, None


def validate_json(input, schema):
    v = Draft4Validator(schema)

    valid = True

    for error in sorted(v.iter_errors(input), key=str):
        valid = False
        common.log_error("JSON Validation ERROR: " + error.message)

    return valid


def get_version(payload, version_key_name):
    try:
        version = payload["version"][version_key_name]
    except KeyError:
        version = None
    return version


def versions_as_list(versions, version_key_name):
    if versions is None:
        return json.dumps([])
    else:
        version_dictionary = []
        for version in versions:
            version_dictionary.append({version_key_name: version})
        return json.dumps(version_dictionary)


def get_version_output(version, version_key_name):
    if version is None:
        return [{}]
    else:
        return json.dumps({"version": {version_key_name: version}})


def contains_params_key(payload, key_name):
    return key_name in payload['params']


def get_source_value(payload, key):
    try:
        return payload['source'][key]
    except KeyError:
        return None


def get_params_value(payload, key):
    try:
        return payload['params'][key]
    except KeyError:
        return None
