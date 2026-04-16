import unittest
from datetime import datetime
from driven import clean_email_data, generate_messages
class TestStaffDataProcessing(unittest.TestCase):
    
    def test_clean_email_data(self):
        raw_data = [
            "john.doe@company..com, 1985-07-23, 2015-06-15, Software Engineer!!",
            "JANE_DOE@@company.com, 1990-12-05, 2018-09-01, Senior Manager**",
            "BOB.SMITH#company.com, 1975-04-17, 2000-03-12, CTO@@",
        ]
        expected_cleaned_data = [
            {"email": "john.doe@company.com", "birth_date": "1985-07-23", "start_date": "2015-06-15", "title": "Software Engineer"},
            {"email": "jane_doe@company.com", "birth_date": "1990-12-05", "start_date": "2018-09-01", "title": "Senior Manager"},
            {"email": "bob.smith@company.com", "birth_date": "1975-04-17", "start_date": "2000-03-12", "title": "CTO"},
        ]
        
        cleaned_data = clean_email_data(raw_data)  # This function must be implemented
        self.assertEqual(cleaned_data, expected_cleaned_data)
    
    def test_generate_messages(self):
        structured_data = [
            {"email": "john.doe@company.com", "birth_date": "1985-07-23", "start_date": "2015-06-15", "title": "Software Engineer"},
            {"email": "jane_doe@company.com", "birth_date": "1990-12-05", "start_date": "2018-09-01", "title": "Senior Manager"},
            {"email": "bob.smith@company.com", "birth_date": "1975-04-17", "start_date": "2000-03-12", "title": "CTO"},
        ]
        today = datetime(2025, 7, 23)  # Simulated current date for testing
        expected_messages = [
            "Happy Birthday, John Doe! Have a fantastic day!",
            "Happy Work Anniversary, John Doe! 10 years at the company!",
        ]
        
        messages = generate_messages(structured_data, today)  # This function must be implemented
        
        for msg in expected_messages:
            self.assertIn(msg, messages)
    
    def test_no_messages_for_non_matching_dates(self):
        structured_data = [
            {"email": "john.doe@company.com", "birth_date": "1985-07-23", "start_date": "2015-06-15", "title": "Software Engineer"},
            {"email": "jane_doe@company.com", "birth_date": "1990-12-05", "start_date": "2018-09-01", "title": "Senior Manager"},
            {"email": "bob.smith@company.com", "birth_date": "1975-04-17", "start_date": "2000-03-12", "title": "CTO"},
        ]
        today = datetime(2025, 8, 15)  # A date that doesn't match any events
        messages = generate_messages(structured_data, today)
        self.assertEqual(messages, [])  # No messages should be generated

if __name__ == '__main__':
    unittest.main()