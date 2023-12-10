import os
import unittest


def load_tests(loader, tests, pattern):
    top_level_dir = os.path.dirname(__file__)
    pattern = "test_*.py"
    exclude_files = ["test_oauth", "test_async_oauth"]
    suite = unittest.TestSuite()

    # using loader.discover to find all test modules
    discovered_suite = loader.discover(top_level_dir, pattern=pattern)

    # add all tests to the suite
    for test in discovered_suite:
        if any(exclude_file in str(test) for exclude_file in exclude_files):
            continue
        suite.addTest(test)

    return suite
