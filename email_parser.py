#!/usr/bin/env python3
"""
Crescent Scorecard Email Parser
Automatically parse shift report emails and update Firebase
"""

import re
import json
from datetime import datetime, timedelta
import requests
from email import message_from_string
import imaplib
import os
from typing import Dict, Optional

# Configuration
FIREBASE_URL = "https://YOUR_PROJECT.firebaseio.com"
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT", "your-email@example.com")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "your-app-password")
IMAP_SERVER = "imap.gmail.com"  # Change for different email provider

class ShiftDataParser:
    """Parse shift data from email content"""
    
    @staticmethod
    def parse_date(text: str) -> Optional[str]:
        """Extract and format date from email"""
        patterns = [
            r'Date:\s*(\d{1,2}[/-]\d{1,2}[/-]\d{4})',  # Date: 11/19/2025
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})',  # 11/19/2025
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                date_str = match.group(1)
                # Convert to YYYY-MM-DD format
                try:
                    date_obj = datetime.strptime(date_str.replace('-', '/'), '%m/%d/%Y')
                    return date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    continue
        return None
    
    @staticmethod
    def parse_shift(text: str) -> Optional[str]:
        """Extract shift (1st or 2nd) from email"""
        match = re.search(r'Shift:\s*(1st|2nd|first|second)', text, re.IGNORECASE)
        if match:
            shift = match.group(1).lower()
            if shift in ['1st', 'first']:
                return '1st'
            elif shift in ['2nd', 'second']:
                return '2nd'
        return None
    
    @staticmethod
    def parse_number(text: str, field_name: str) -> int:
        """Extract numeric value for a specific field"""
        pattern = rf'{field_name}:\s*(\d+)'
        match = re.search(pattern, text, re.IGNORECASE)
        return int(match.group(1)) if match else 0
    
    @staticmethod
    def parse_decimal(text: str, field_name: str) -> float:
        """Extract decimal value for a specific field"""
        pattern = rf'{field_name}:\s*([\d.]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        return float(match.group(1)) if match else 0.0
    
    def parse_email(self, email_body: str) -> Optional[Dict]:
        """Parse complete shift data from email body"""
        date = self.parse_date(email_body)
        shift = self.parse_shift(email_body)
        
        if not date or not shift:
            print(f"Could not parse date ({date}) or shift ({shift})")
            return None
        
        data = {
            'forecasted': self.parse_number(email_body, 'Forecasted'),
            'requested': self.parse_number(email_body, 'Requested'),
            'required': self.parse_number(email_body, 'Required'),
            'working': self.parse_number(email_body, 'Working'),
            'newStarts': self.parse_number(email_body, 'New Starts'),
            'sentHome': self.parse_number(email_body, 'Sent Home'),
            'directHours': self.parse_decimal(email_body, 'Direct Hours'),
            'surveysCompleted': self.parse_number(email_body, 'Surveys Completed'),
            'earlyLeaves': self.parse_number(email_body, 'Early Leaves'),
            'dnrs': self.parse_number(email_body, 'DNRs'),
        }
        
        return {
            'date': date,
            'shift': shift,
            'data': data
        }

class FirebaseUpdater:
    """Update Firebase Realtime Database with shift data"""
    
    def __init__(self, firebase_url: str):
        self.base_url = firebase_url.rstrip('/')
    
    @staticmethod
    def get_week_ending(date_str: str) -> str:
        """Calculate week ending date (Sunday) for a given date"""
        date = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_week = date.weekday()
        # weekday(): Mon=0, Tue=1, ..., Sun=6
        days_until_sunday = (6 - day_of_week) % 7
        week_ending = date + timedelta(days=days_until_sunday)
        return week_ending.strftime('%Y-%m-%d')
    
    def update_shift_data(self, date: str, shift: str, data: Dict) -> bool:
        """Update shift data in Firebase"""
        week_ending = self.get_week_ending(date)
        url = f"{self.base_url}/scorecard/{week_ending}/{date}/{shift}.json"
        
        try:
            response = requests.put(url, json=data)
            response.raise_for_status()
            print(f"✓ Updated {date} {shift} shift successfully")
            return True
        except requests.exceptions.RequestException as e:
            print(f"✗ Error updating Firebase: {e}")
            return False

class EmailFetcher:
    """Fetch emails from IMAP server"""
    
    def __init__(self, server: str, email: str, password: str):
        self.server = server
        self.email = email
        self.password = password
    
    def fetch_unread_emails(self, subject_filter: str = None):
        """Fetch unread emails, optionally filtered by subject"""
        try:
            mail = imaplib.IMAP4_SSL(self.server)
            mail.login(self.email, self.password)
            mail.select('inbox')
            
            # Search for unread emails
            search_criteria = '(UNSEEN)'
            if subject_filter:
                search_criteria = f'(UNSEEN SUBJECT "{subject_filter}")'
            
            status, messages = mail.search(None, search_criteria)
            email_ids = messages[0].split()
            
            emails = []
            for email_id in email_ids:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                email_body = msg_data[0][1].decode('utf-8')
                msg = message_from_string(email_body)
                
                # Get email body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode('utf-8')
                            break
                else:
                    body = msg.get_payload(decode=True).decode('utf-8')
                
                emails.append({
                    'id': email_id,
                    'subject': msg['subject'],
                    'from': msg['from'],
                    'body': body
                })
            
            mail.close()
            mail.logout()
            
            return emails
            
        except Exception as e:
            print(f"Error fetching emails: {e}")
            return []
    
    def mark_as_read(self, email_id: bytes):
        """Mark an email as read"""
        try:
            mail = imaplib.IMAP4_SSL(self.server)
            mail.login(self.email, self.password)
            mail.select('inbox')
            mail.store(email_id, '+FLAGS', '\\Seen')
            mail.close()
            mail.logout()
        except Exception as e:
            print(f"Error marking email as read: {e}")

def process_emails():
    """Main function to process shift report emails"""
    print("=" * 50)
    print("Crescent Scorecard Email Processor")
    print("=" * 50)
    
    parser = ShiftDataParser()
    firebase = FirebaseUpdater(FIREBASE_URL)
    fetcher = EmailFetcher(IMAP_SERVER, EMAIL_ACCOUNT, EMAIL_PASSWORD)
    
    # Fetch emails with "Shift Report" in subject
    emails = fetcher.fetch_unread_emails("Shift Report")
    print(f"\nFound {len(emails)} unread shift report emails")
    
    for email_data in emails:
        print(f"\nProcessing: {email_data['subject']}")
        
        # Parse shift data
        parsed = parser.parse_email(email_data['body'])
        
        if parsed:
            # Update Firebase
            success = firebase.update_shift_data(
                parsed['date'],
                parsed['shift'],
                parsed['data']
            )
            
            if success:
                # Mark email as read
                fetcher.mark_as_read(email_data['id'])
            
            # Print summary
            print(f"  Date: {parsed['date']}")
            print(f"  Shift: {parsed['shift']}")
            print(f"  Working: {parsed['data']['working']} / Required: {parsed['data']['required']}")
            print(f"  Fill Rate: {(parsed['data']['working'] / parsed['data']['required'] * 100) if parsed['data']['required'] else 0:.1f}%")
        else:
            print("  ✗ Could not parse email")
    
    print("\n" + "=" * 50)
    print("Processing complete!")
    print("=" * 50)

def test_parser():
    """Test the parser with sample email"""
    sample_email = """
    Subject: Shift Report - 11/19/2025 - 1st Shift
    
    Date: 11/19/2025
    Shift: 1st
    
    STAFFING:
    Forecasted: 105
    Requested: 99
    Required: 107
    Working: 80
    
    ACTIVITY:
    New Starts: 3
    Sent Home: 0
    Direct Hours: 769.75
    
    QUALITY:
    Surveys Completed: 0
    Early Leaves: 6
    DNRs: 1
    """
    
    parser = ShiftDataParser()
    result = parser.parse_email(sample_email)
    
    print("Test Parser Results:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_parser()
    else:
        # Check if credentials are set
        if EMAIL_ACCOUNT == "your-email@example.com" or not EMAIL_PASSWORD:
            print("Error: Please set EMAIL_ACCOUNT and EMAIL_PASSWORD environment variables")
            print("\nExample:")
            print("export EMAIL_ACCOUNT='your-email@gmail.com'")
            print("export EMAIL_PASSWORD='your-app-password'")
            print("\nFor Gmail, use an App Password: https://support.google.com/accounts/answer/185833")
            sys.exit(1)
        
        if FIREBASE_URL == "https://YOUR_PROJECT.firebaseio.com":
            print("Error: Please update FIREBASE_URL in the script")
            sys.exit(1)
        
        process_emails()
