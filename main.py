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
PASSWORD = PASSWORD = str(os.getenv("MY_PASSWORD"))
def birthday(lists_of_data,today,this_month):
    listname = [First_name for First_name, days, months in zip(lists_of_data.name, lists_of_data.day, lists_of_data.month)
                if days == today and months == this_month
                ]
    listemail =[emails for emails, days, months in zip(lists_of_data.email, lists_of_data.day, lists_of_data.month)
        if days == today and months == this_month
                ]
    return listname,listemail

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
                letter_templates=['letter_1.txt','letter_2.txt','letter_3.txt']
                picks_ran_letter=random.choice(letter_templates)
                for names in name:
                    with open(f"letter_templates/{picks_ran_letter}","r") as f:
                        content = f.read()
                        letter=content.replace("[NAME]",f"{names}")
                        print(letter)
                    for email in email_list:
                        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                            connection.starttls()
                            connection.login(user=my_email, password=PASSWORD)
                            message = f"Subject: birthday greetings\n\n{letter}"
                            connection.sendmail(from_addr=my_email, to_addrs=email, msg=message)
                            print(f"Email sent to {email}")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
