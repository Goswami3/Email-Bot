import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
from dotenv import load_dotenv  # pip install python-dotenv

PORT = 587
EMAIL_SERVER = "smtp.gmail.com"

# Load the environment variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
if envars.exists():
    load_dotenv(envars)
else:
    raise FileNotFoundError(f"Environment file not found at {envars}")

# Read environment variables
sender_email = os.getenv("email")
password_email = os.getenv("password")

if not sender_email or not password_email:
    raise ValueError("Email credentials are not set in the environment variables.")


def send_email(subject, receiver_email, name, date, order_no, amount):
    # Create the base text message
    msg = EmailMessage()
    msg["subject"] = subject
    msg["From"] = formataddr(("Python Corp.", f"{sender_email}"))
    msg["To"] = receiver_email

    msg.set_content(
        f"""\
Hi {name},
Thank you for shopping with us at Salty! We just wanted to drop a quick note to remind you that you have now collected {amount} points 
in your Saltywallet as per your transaction for order number {order_no} on date {date}.
We would really appreciate if you would provide a confirmation to continue availing our wallet facility for further discounts using your wallet points.
Kindly reply 1 to this email to confirm by midnight.
Best Regards
AVILASHA GOSWAMI
Team, Salty
"""
    )

    # Add the HTML version
    msg.add_alternative(
        f"""\
<html>
    <body>
        <p>Hi {name}</p>
        <p>Thank you for shopping with us at Salty!</p>
        <p>We just wanted to drop a quick note to remind you that you have now collected <strong>{amount}</strong> points 
        in your Saltywallet as per your transaction for order number <strong>{order_no}</strong> on date <strong>{date}</strong>.</p>
        <p>We would really appreciate if you would provide a confirmation to continue availing our wallet facility 
        for further discounts using your wallet points.</p>
        <p>Kindly reply 1 to this email to confirm by midnight.</p>
        <p>Best Regards</p>
        <p>AVILASHA GOSWAMI</p>
        <p>Team, Salty</p>
    </body>
</html>
""",
        subtype="html",
    )

    try:
        with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
            server.starttls()
            server.login(sender_email, password_email)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    send_email(
        subject="SaltyWallet",
        name="Avilasha Goswami",
        receiver_email="avilasha2411@gmail.com",
        date="06 Dec, 2024",
        order_no="154-17-009",
        amount="5",
    )
