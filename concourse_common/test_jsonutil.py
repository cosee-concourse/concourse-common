import unittest

from concourse_common import jsonutil, testutil, schemas, request


class TestJsonUtil(unittest.TestCase):
    VERSION_KEY_NAME = 'version'

    check_payload = ('{"source":{'
                     '"bucket":"bucketName",'
                     '"access_key_id":"apiKey123",'
                     '"secret_access_key":"secretKey321",'
                     '"region_name":"eu-west-1",'
                     '"filename":"release-'
                     '"},'
                     '"version":{"version":"version-v1-dev"}}')
    check_payload_without_version = ('{"source":{'
                                     '"bucket":"bucketName",'
                                     '"access_key_id":"apiKey123",'
                                     '"secret_access_key":"secretKey321",'
                                     '"region_name":"eu-west-1",'
                                     '"filename":"release-'
                                     '"}}')
    invalid_payload = ('{"sourcez":{'
                       '"bucket":"bucketName",'
                       '"access_key_id":"apiKey123",'
                       '"secret_access_key":"secretKey321",'
                       '"region_name":"eu-west-1",'
                       '"filename":"release-'
                       '"},'
                       '"version":{"version":"version-v1-dev"}}')

    test_json_payload = {'source': {'bucket': 'bucketName', 'access_key_id': 'apiKey123', 'secret_access_key':
        'secretKey321', 'region_name': 'eu-west-1', 'filename': 'release-'}, 'version': {'version': 'version-v1-dev'}}

    test_json_payload_with_params = {'source': {'bucket': 'bucketName', 'access_key_id': 'apiKey123', 'secret_access_key':
        'secretKey321', 'region_name': 'eu-west-1', 'filename': 'release-'}, 'params': {'some_parameter': 'value'},
                                     'version': {'version': 'version-v1-dev'}}

    test_json_payload_without_version = {'source': {'bucket': 'bucketName', 'access_key_id': 'apiKey123',
                                                    'secret_access_key': 'secretKey321', 'region_name': 'eu-west-1',
                                                    'filename': 'release-'}}


    def test_json_empty_version(self):
        output = jsonutil.versions_as_list(None, self.VERSION_KEY_NAME)
        self.assertEqual(output, "[]")

    def test_json_with_version(self):
        output = jsonutil.versions_as_list(["version-v1-dev"], self.VERSION_KEY_NAME)
        self.assertEqual(output, '[{"version": "version-v1-dev"}]')

    def test_json_with_multiple_versions(self):
        output = jsonutil.versions_as_list(["1.0.0", "1.0.1"], self.VERSION_KEY_NAME)
        self.assertEqual(output, '[{"version": "1.0.0"}, {"version": "1.0.1"}]')

    def test_json_version_output(self):
        output = jsonutil.get_version_output("version-v1-dev", self.VERSION_KEY_NAME)
        self.assertEqual(output, '{"version": {"version": "version-v1-dev"}}')

    def test_get_payload(self):
        testutil.put_stdin(self.check_payload)
        result = jsonutil.load_payload()
        self.assertEqual(result, self.test_json_payload)

    def test_validates_json_valid_result(self):
        testutil.put_stdin(self.check_payload)
        payload = jsonutil.load_payload()

        self.assertTrue(jsonutil.validate_json(payload, schemas.test_schema))

    def test_validates_json_valid_result_without_version(self):
        testutil.put_stdin(self.check_payload_without_version)
        payload = jsonutil.load_payload()

        self.assertTrue(jsonutil.validate_json(payload, schemas.test_schema))

    def test_validates_json_invalid_result(self):
        testutil.put_stdin(self.invalid_payload)
        payload = jsonutil.load_payload()

        self.assertFalse(jsonutil.validate_json(payload, schemas.test_schema))

    def test_load_and_validate_payload_valid(self):
        testutil.put_stdin(self.check_payload)
        valid, payload = jsonutil.load_and_validate_payload(schemas, request.Request.CHECK)
        self.assertTrue(valid)
        self.assertEqual(payload, self.test_json_payload)

    def test_load_and_validate_payload_invalid(self):
        testutil.put_stdin(self.invalid_payload)
        valid, payload = jsonutil.load_and_validate_payload(schemas, request.Request.CHECK)
        self.assertFalse(valid)
        self.assertIsNone(payload)

    def test_get_version(self):
        output = jsonutil.get_version(self.test_json_payload, "version")
        self.assertEqual(output, 'version-v1-dev')

    def test_get_version_without_version(self):
        output = jsonutil.get_version(self.test_json_payload_without_version, "version")
        self.assertIsNone(output)

    def test_contains_params_key(self):
        output = jsonutil.contains_params_key(self.test_json_payload_with_params, 'some_parameter')
        self.assertTrue(output)

    def test_get_source_value(self):
        output = jsonutil.get_source_value(self.test_json_payload, 'bucket')
        self.assertEqual(output, 'bucketName')

    def test_get_params_value(self):
        output = jsonutil.get_params_value(self.test_json_payload_with_params, 'some_parameter')
        self.assertEqual(output, 'value')