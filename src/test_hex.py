from .hex import HexFile, HexConverter

import unittest, os, string
from enum import Enum

TESTDATA_PATH = os.path.join(os.path.dirname(__file__), "testdata")
HEX_DATA = ['54', '65', '73', '74', '20', '31', '32', '33', '21', '9', 'A', '31', '32', '33', '35', '40', '40']
ASCII_DATA = ['T', 'e', 's', 't', '.', '1', '2', '3', '!', '.', '.', '1', '2', '3', '5', '@', '@']

class TestDataSpecialChars(Enum):
    Bytes = b'\t\n\r\x0b\x0c\x00\x20'
    Hex = ['9', 'A', 'D', 'B', 'C', '00', '20']
    Text = ['.', '.', '.', '.', '.', '.', '.']

class TestDataAsciiChars(Enum):
    Bytes = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
    Hex = ['30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '61', '62', '63', '64', '65', '66', '67', 
        '68', '69', '6A', '6B', '6C', '6D', '6E', '6F', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', 
        '7A', '41', '42', '43', '44', '45', '46', '47', '48', '49', '4A', '4B', '4C', '4D', '4E', '4F', '50', '51', 
        '52', '53', '54', '55', '56', '57', '58', '59', '5A', '21', '22', '23', '24', '25', '26', '27', '28', '29', 
        '2A', '2B', '2C', '2D', '2E', '2F', '3A', '3B', '3C', '3D', '3E', '3F', '40', '5B', '5C', '5D', '5E', '5F', 
        '60', '7B', '7C', '7D', '7E']
    Text = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'

class TestHexFile(unittest.TestCase):
    def testInit(self) -> None:
        with open(TESTDATA_PATH, "w") as f:
            f.write("Test")

        self.assertEqual(HexConverter(content=b"Test").bytes, HexFile(path=TESTDATA_PATH).converter.bytes)

    def testWrongPath(self) -> None:
        self.assertRaises(FileNotFoundError, HexFile, "blahblahblah")
    
    def testWrongPathType(self) -> None:
        self.assertRaises(ValueError, HexFile, True)
        self.assertRaises(ValueError, HexFile, 123)
        self.assertRaises(ValueError, HexFile, b"blah")
    
    def testEmptyFile(self) -> None:
        with open(TESTDATA_PATH, "w") as f:
            f.write("")

        file = HexFile(path=TESTDATA_PATH)
        file.converter = HexConverter(content=b"")

        self.assertListEqual([], file.hex)
        self.assertListEqual([], file.ascii)
    
    def testCorrect(self) -> None:
        with open(TESTDATA_PATH, "w")as f:
            f.write("Test 123!\t\n1235@@")

        file = HexFile(path=TESTDATA_PATH)
        
        self.assertListEqual(HEX_DATA, file.hex)
        self.assertListEqual(ASCII_DATA, file.ascii)

class TestHexConverter(unittest.TestCase):
    def testInit(self) -> None:
        testData = b"12345"
        self.assertEqual(testData, HexConverter(content=testData).bytes)

    def testWrongType(self) -> None:
        self.assertRaises(ValueError, HexConverter, "blah")
        self.assertRaises(ValueError, HexConverter, True)
        self.assertRaises(ValueError, HexConverter, 123)
    
    def testEmptyData(self) -> None:
        converter = HexConverter(content=b"")

        self.assertListEqual([], converter.hex())
        self.assertListEqual([], converter.ascii())

    def testAsciiConversion(self) -> None:
        converter = HexConverter(content=TestDataAsciiChars.Bytes.value)
        
        self.assertEqual(TestDataAsciiChars.Hex.value, converter.hex())
        self.assertEqual(TestDataAsciiChars.Text.value, "".join(converter.ascii()))
    
    def testSpecialConversion(self) -> None:
        converter = HexConverter(content=TestDataSpecialChars.Bytes.value)
        
        self.assertEqual(TestDataSpecialChars.Hex.value, converter.hex())
        self.assertEqual(TestDataSpecialChars.Text.value, converter.ascii())
