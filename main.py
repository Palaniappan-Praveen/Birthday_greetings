import datetime as dt
import random
import smtplib
import pandas as pd
import os
now = dt.datetime.now()
year = now.year
month = now.month
day = now.day
#print(day)
#print(month)
my_email = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("MY_PASSWORD")
if not my_email or not PASSWORD:
    raise ValueError("MY_EMAIL and MY_PASSWORD environment variables must be set")
def birthday(df, today, this_month):
    # Ensure columns are integers for comparison
    df['day'] = df['day'].astype(int)
    df['month'] = df['month'].astype(int)

    # Filter rows where month and day match today
    birthday_row = df[(df["month"] == this_month) & (df["day"] == today)]

    # Return lists of names and emails
    return birthday_row["name"].tolist(), birthday_row["email"].tolist()

try :
    data = pd.read_csv('birthdays.csv')

except FileNotFoundError:
    print("No birthdays file found")
else:
    try:
    
        records_old = data.to_dict(orient="records")
        lists = pd.DataFrame(records_old)
        if len(lists) > 0:
            lists.to_csv("birthday.csv", index=False)
            print("birthday file saved")
            list_data=pd.read_csv('birthday.csv')
            records_new = list_data.to_dict(orient="records")
            list_of_data = pd.DataFrame(records_new)
            name,email_list=birthday(list_of_data,day,month)
            print(name)
            if len(name) > 0 and len(email_list) > 0:
                for names, email in zip(name, email_list):
                    letter_templates = ['letter_1.txt', 'letter_2.txt', 'letter_3.txt']
                    with open(f"letter_templates/letter_{random.randint(1,3)}.txt", "r") as f:
                        content = f.read()
                        letter = content.replace("[NAME]", names)

                    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                        connection.starttls()
                        connection.login(user=my_email, password=PASSWORD)
                        message = f"Subject: Birthday Greetings\n\n{letter}"
                        connection.sendmail(from_addr=my_email, to_addrs=email, msg=message)
                        print(f"Email sent to {email}")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
