import unittest
import datetime
import requests
from util import (
    check_for_dolar_sign,
    date_limit,
    format_date,
    count_matches,
)
class TestDolarSign(unittest.TestCase):
    
    def test_format1(self):
        result = check_for_dolar_sign("$11.1")
        self.assertEqual(result, True)
    
    def test_format2(self):
        result = check_for_dolar_sign("$111,111.11")
        self.assertEqual(result, True)
  
    def test_format3(self):
        result = check_for_dolar_sign("11 dollars")
        self.assertEqual(result, True)

    def test_format4(self):
        result = check_for_dolar_sign("11 USD")
        self.assertEqual(result, True)

    def test_format5(self):
        result = check_for_dolar_sign("11 BRL")
        self.assertEqual(result, False)

    def test_format_date_minute(self):
        result = format_date("1 minute ago").strftime("%m/%d/%Y")
        expected = datetime.datetime.now() -  datetime.timedelta(minutes=1)
        self.assertEqual(result, expected.strftime("%m/%d/%Y"))

    def test_format_date_hour(self):
        result = format_date("1 hour ago").strftime("%m/%d/%Y")
        expected = datetime.datetime.now() -  datetime.timedelta(hours=1)
        self.assertEqual(result, expected.strftime("%m/%d/%Y"))

    def test_format_date_week(self):
        result = format_date("1 week ago").strftime("%m/%d/%Y")
        expected =datetime.datetime.now() -  datetime.timedelta(weeks=1)
        self.assertEqual(result, expected.strftime("%m/%d/%Y"))
            
    def test_format_date_minutes(self):
        result = format_date("1 minutes ago").strftime("%m/%d/%Y")
        expected = datetime.datetime.now() -  datetime.timedelta(minutes=1)
        self.assertEqual(result, expected.strftime("%m/%d/%Y"))

    def test_format_date_hours(self):
        result = format_date("5 hours ago").strftime("%m/%d/%Y")
        expected = datetime.datetime.now() -  datetime.timedelta(hours=5)
        self.assertEqual(result, expected.strftime("%m/%d/%Y"))

    def test_format_date_fulldate(self):
        result = format_date("July 15, 2024").strftime("%m/%d/%Y")
        expected = datetime.datetime(2024, 7, 15)
        self.assertEqual(result, expected.strftime("%m/%d/%Y"))    

if __name__ == '__main__':
    unittest.main()