import unittest
import datetime
import requests
from dateutil.relativedelta import relativedelta
from util import (
    check_for_dolar_sign,
    date_limit,
    format_date,
    count_matches,
)
class TestDolarSign(unittest.TestCase):
    
    #Test_check_for_dolar_sign
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

    #Test_Format_Date
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

    def test_format_date_limit(self):
        result = date_limit(0)
        expected = datetime.datetime.today().replace(day=1)
        self.assertEqual(result.strftime("%m/%d/%Y"), expected.strftime("%m/%d/%Y"))    


    #Date_limit
    def test_format_date_limit0(self):
        result = date_limit(0)
        expected = datetime.datetime.today().replace(day=1)
        self.assertEqual(result, expected)   

    def test_format_date_limit1(self):
        result = date_limit(1)
        expected = datetime.datetime.today().replace(day=1)
        self.assertEqual(result, expected)   

    def test_format_date_limit5(self):
        result = date_limit(5).strftime("%m/%d/%Y")
        expected = datetime.datetime.today().replace(day=1) - relativedelta(months =5)
        self.assertEqual(result, expected.strftime("%m/%d/%Y"))

    #Test_Count_Matches
    def test_count_matches1(self):
        result = count_matches("Business","This is a Business article")
        expected = 1
        self.assertEqual(result, expected)   

    def test_count_matches2(self):
        result = count_matches("Business","This is a Busines article")
        expected = 0
        self.assertEqual(result, expected)   

    def test_count_matches3(self):
        result = count_matches("Business","ThisisaBusinessarticle")
        expected = 0
        self.assertEqual(result, expected)   

    def test_count_matches3(self):
        result = count_matches("Business","This is a Business Business article")
        expected = 2
        self.assertEqual(result, expected)   






if __name__ == '__main__':
    unittest.main()