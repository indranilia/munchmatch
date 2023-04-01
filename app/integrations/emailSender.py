import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from os import environ as env
import os
import re

# Load environment variables from .env file
load_dotenv()


async def sendEmail(receiver_email, subject, type, firstName, link):
    """
    Sends an email with HTML content to the specified receiver email address.

    Args:
        receiver_email: A string representing the email address of the recipient.
        subject: A string representing the subject of the email message.
        type: A string representing the type of email template to use.
        firstName: A string representing the first name of the recipient.
        link: A string representing a link to include in the email message.

    Returns:
        None.
    """
    sender_email = env['EMAIL_ADDRESS']
    password = env['EMAIL_PASSWORD']

    # Define a regex pattern to match placeholders to replace in the email template
    regex_pattern = r"\${firstName}|\${link}"
    # Define a dictionary of replacement strings for each matched placeholder
    replacement_strings = {"${firstName}": firstName, "${link}": link}
    # Define a function to replace matched placeholders with corresponding strings

    def replace(match):
        return replacement_strings[match.group(0)]

    # Read the HTML email template file and replace placeholders with actual values
    html = open(os.getcwd()+f'/app/templates/emails/{type}.html')
    htmlString = re.sub(regex_pattern, replace, html.read())

    # Create the email message object
    message = MIMEText(htmlString, 'html')
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    html.close()

    try:
        # Create secure connection with server and send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            await server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

        return 'Sent!'
    except Exception as error:
        return error
