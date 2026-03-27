# to loop over our spreadsheet and send emails if our conditions are met
from datetime import date  # core python module
import pandas as pd  # pip install pandas
from send_email import send_email  # local python module

# converting google sheets document to a csv file
SHEET_ID = "1vDaOoAn5LXgWxHxtn5RgXPpRh--dwoWRziCkZUn1tlU"
SHEET_NAME = "Sheet1"
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# function to convert
def load_df(url):
    parse_dates = ["date", "reminder_date"]
    df = pd.read_csv(url, parse_dates=parse_dates)  # Include 'url' as the first parameter
    return df




# querying the data
# function to check if we need to send the email today
def query_data_and_send_emails(df):
    present = date.today()
    email_counter = 0
    for _, row in df.iterrows():
        if(present >= row["reminder_date"].date()) and (row["confirmed"]=="no"):
            send_email (
                subject = f'[Python Corp.] Reminder : SaltyWallet',
                receiver_email = row["email"],
                name = row["name"],
                date = row["date"].strftime("%d %b %Y"),  # date-time converted into readable form example: 11, Aug 2022
                order_no = row["order_no"],
                amount = row["amount"],
            ) 
            email_counter += 1
    return f"Total emails sent: {email_counter}"

df = load_df(URL)
result = query_data_and_send_emails(df)
print(result)