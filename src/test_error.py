from error import ErrorHandler

import unittest, os

TESTDATA_REPORT = "This is a basic test report"
TESTDATA_PATH = os.path.join(os.path.dirname(__file__), "testreport")

class TestErrorHandler(unittest.TestCase):
    def testWrongPath(self) -> None:
        self.assertRaises(FileNotFoundError, ErrorHandler, "blahblahblah")

    def testWrongPathType(self) -> None:
        self.assertRaises(ValueError, ErrorHandler, True)
        self.assertRaises(ValueError, ErrorHandler, 123)
        self.assertRaises(ValueError, ErrorHandler, b"blah")

    def testWrongType(self) -> None:
        handler = ErrorHandler(output_path=TESTDATA_PATH)

        self.assertRaises(ValueError, handler.handleError, "NotAnError", "Message")
        self.assertRaises(ValueError, handler.handleError, 123, "Message")
        self.assertRaises(ValueError, handler.handleError, BaseException, 123)
        self.assertRaises(ValueError, handler.handleError, BaseException, True)
        self.assertRaises(ValueError, handler.handleError, BaseException, b"Message")

    def testEmptyMessage(self) -> None:
        handler = ErrorHandler(output_path=TESTDATA_PATH)
        self.assertRaises(TypeError, handler.handleError, BaseException, "")

    def testCorrectReport(self) -> None:
        handler = ErrorHandler(output_path=TESTDATA_PATH)
        self.assertEqual(TESTDATA_REPORT, handler._generateReport(FileNotFoundError, "Couldn't find the file"))
    
    def testCorrectPrinting(self) -> None:
        with open(TESTDATA_PATH, "w") as f:
            f.write("Nothing in this file")

        handler = ErrorHandler(output_path=TESTDATA_PATH)
        handler._printReport(TESTDATA_REPORT)

        with open(TESTDATA_PATH) as f:
            self.assertEqual(f.read(), TESTDATA_REPORT)

    def testAllCorrect(self) -> None:
        with open(TESTDATA_PATH, "w") as f:
            f.write("Nothing in this file")

        handler = ErrorHandler(output_path=TESTDATA_PATH)
        handler.handleError(FileNotFoundError, "Couldn't find the file")
        with open(TESTDATA_PATH) as f:
            self.assertEqual(f.read(), TESTDATA_REPORT)
