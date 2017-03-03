source_schema = {
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

version_schema = {
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

test_schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        "source": source_schema,
        "version": version_schema
    },
    "required": [
        "source"
    ]
}

check_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "properties": {
    "source": {
      "type": "object",
      "properties": {
        "secret_access_key": {
          "type": "string"
        },
        "filename": {
          "type": "string"
        },
        "access_key_id": {
          "type": "string"
        },
        "bucket": {
          "type": "string"
        },
        "region_name": {
          "type": "string"
        }
      },
      "required": [
        "secret_access_key",
        "filename",
        "access_key_id",
        "bucket",
        "region_name"
      ]
    },
    "version": {
      "type": "object",
      "properties": {
        "version": {
          "type": "string"
        }
      },
      "required": [
        "version"
      ]
    }
  },
  "required": [
    "source"
  ]
}