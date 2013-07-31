import re
import uuid


def make_uuid():
    return uuid.uuid1()


def is_uuid(uuid_str):
    if isinstance(uuid_str, uuid.UUID):
        uuid_str = str(uuid_str)
    if uuid_str is None or not isinstance(uuid_str, basestring):
        return False
    re_string = r"%s-%s-%s-%s-%s" % ("^[0-9a-f]{8}",
                                     "[0-9a-f]{4}",
                                     "[1-5][0-9a-f]{3}",
                                     "[89ab][0-9a-f]{3}",
                                     "[0-9a-f]{12}$")
    m = re.match(re_string, uuid_str)
    if not m:
        return False
    return m.group(0) == uuid_str
