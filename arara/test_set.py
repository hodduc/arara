import unittest
import test

import test.article_manager_test
import test.blacklist_manager_test
import test.board_manager_test
import test.file_manager_test
import test.login_manager_test
import test.member_manager_test
import test.messaging_manager_test
import test.model_test
import test.read_status_manager_test

def suite():
    return unittest.TestSuite([
        test.article_manager_test.suite(),
        test.blacklist_manager_test.suite(),
        test.board_manager_test.suite(),
        test.file_manager_test.suite(),
        test.login_manager_test.suite(),
        test.member_manager_test.suite(),
        test.messaging_manager_test.suite(),
        test.model_test.suite(),
        test.read_status_manager_test.suite()
        ])

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=1).run(suite())
