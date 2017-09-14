import re
from os import path, listdir
import sys

#
# Precompiled patterns for performance
#
date_pattern = re.compile("Date: (?P<data>[A-Z][a-z]+\, \d{1,2} [A-Z][a-z]+ \d{4} \d{2}\:\d{2}\:\d{2} \-\d{4} \([A-Z]{3}\))")
subject_pattern = re.compile("Subject: (?P<data>.*)")
sender_pattern = re.compile("X-From: (?P<data>.*)")
recipients_pattern = re.compile("X-To: (?P<data>.*)")
cc_pattern = re.compile("X-cc: (?P<data>.*)")
bcc_pattern = re.compile("X-bcc: (?P<data>.*)")
msg_start_pattern = re.compile("\n\n", re.MULTILINE)
msg_end_pattern = re.compile("\n+.*\n\d+/\d+/\d+ \d+:\d+ [AP]M", re.MULTILINE)

def parse_email(pathname):
    """
    Receives a folder name, recursively parses subfolders for email data
    Returns a list of json objects representing emails
    """
    if path.isdir(pathname):
        emails = []
        for child in listdir(pathname):
            # only parse visible files
            if child[0] != ".":
                child_parse = parse_email(path.join(pathname, child))
                if type(child_parse) == list and len(child_parse) > 0:
                     emails += child_parse
                elif type(child_parse) == dict:
                     emails.append(child_parse)
        return emails
    else:
        with open(pathname) as TextFile:
            text = TextFile.read()
            try:
                date = date_pattern.search(text).group("data")
                subject = subject_pattern.search(text).group("data")
                sender = sender_pattern.search(text).group("data")
                recipients = recipients_pattern.search(text).group("data").split(", ")
                cc = cc_pattern.search(text).group("data").split(", ")
                bcc = bcc_pattern.search(text).group("data").split(", ")
                msg_start_iter = msg_start_pattern.search(text).end()
                try:
                    msg_end_iter = msg_end_pattern.search(text).start()
                    message = text[msg_start_iter:msg_end_iter]
                except AttributeError: # not a reply
                    message = text[msg_start_iter:]
            except AttributeError:
                return None

        sender = extract_address(sender)
        cc = extract_email_addresses(cc)
        bcc = extract_email_addresses(bcc)
        recipients = extract_email_addresses(recipients)
        message = message.replace("\n", " ").replace("\r", " ")
        subject = subject.replace("\n", " ").replace("\r", " ")

        return {'date': date, 'subject': subject, 'sender': sender, 'recipients': recipients, 'cc': cc, 'bcc': bcc, 'message': message}

def extract_email_addresses(email_address_list):
    """
    Returns a list of email addresses from a list of email addresses with extra content
    """
    return [extract_address(email_address_list[i]) if "<" in email_address_list[i] else email_address_list[i].replace("\n", " ").replace("\r", " ") for i in range(0, len(email_address_list))]

def extract_address(email_address_text):
    """
    Extracts a single email address from a blob of text
    """
    email_address_text = email_address_text.replace("\n", " ").replace("\r", " ")
    if "<" in email_address_text and ">" in email_address_text:
        return email_address_text[email_address_text.index("<") + 1:email_address_text.index(">"):1]
    else:
        return email_address_text
