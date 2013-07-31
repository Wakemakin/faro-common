import unittest

import faro_common.decorators as dec


class DecoratorTest(unittest.TestCase):

    def test_static_var_decorator(self):
        """Ensure that static variables in functions are carried over."""
        @dec.static_var("c", 0)
        def counting_function():
            counting_function.c += 1
            return counting_function.c
        assert counting_function() == 1
        assert counting_function() == 2
        assert counting_function() == 3
        assert counting_function() == 4
