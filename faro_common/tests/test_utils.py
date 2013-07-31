import unittest
import uuid

import faro_common.utils as utils


class UtilsTest(unittest.TestCase):

    def test_make_uuid(self):
        temp_uuid = utils.make_uuid()
        assert isinstance(temp_uuid, uuid.UUID)
        assert len(str(temp_uuid)) == 36

    def test_make_uuid_uniqueness(self):
        uuids = set([utils.make_uuid() for i in range(100)])
        assert len(uuids) == 100

    def test_uuid_check_valid(self):
        uuids = set([utils.make_uuid() for i in range(100)])
        for uuid in uuids:
            assert utils.is_uuid(uuid)

    def test_uuid_check_invalid(self):
        assert not utils.is_uuid("asdf")
        assert not utils.is_uuid("")
        assert not utils.is_uuid(None)
