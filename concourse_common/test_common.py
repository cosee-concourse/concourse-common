import unittest

from concourse_common import testutil, common


class TestCommon(unittest.TestCase):
    def test_log_on_stderr(self):
        io = testutil.mock_stderr()
        common.log("Some Test Log")
        self.assertEqual("Some Test Log", testutil.read_from_io(io))

    def test_join_paths(self):
        self.assertEqual(common.join_paths("a", "b", "c"), "a/b/c")


if __name__ == '__main__':
    unittest.main()
