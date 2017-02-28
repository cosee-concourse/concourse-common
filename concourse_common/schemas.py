sourceSchema = {
    "type": "object",
    "properties": {
        "access_key_id": {
            "type": "string"
        },
        "secret_access_key": {
            "type": "string"
        },
        "region_name": {
            "type": "string"
        }
    },
    "required": [
        "access_key_id",
        "secret_access_key"
    ]
}

versionSchema = {
    "oneOf": [{
        "type": "object",
        "properties": {
            "schema": {
                "type": "string"
            }
        }
    }, {
        "type": "null"
    }]
}

testSchema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": sourceSchema,
        "version": versionSchema
    },
    "required": [
        "source"
    ]
}