from bs4 import BeautifulSoup
import requests
import time
import datetime
import pandas as pd
import csv
import os
import smtplib
import dotenv

dotenv.load_dotenv()


password = os.getenv('PASSWORD')

def check_price():
# Connect to Website and pull in data
    URL = 'https://www.amazon.com/Data-Science-Programming-Programmer-T-Shirt/dp/B0C1TGFN8M/ref=sr_1_7?crid=2QDSC0MU1AFTY&dib=eyJ2IjoiMSJ9.8S8PRbJgIywHwKobIPqKaIAaiMGQQMpyI5OaQ8p_51uSrreRLr-mIf6Zj04R12ZB3a6PTzXNlNz41aQEirjbEcyvkQ3NiKjiYl8cFrHUF144VOSS7iaANP_zVjTHDZbOqV5k1ZI-OLTgfBwBUSZXv8ULObcfXnKLqWoWTtxHBgqIm85WMZ-0QD6sI2jUDmImRQTob8A274xiFsS7e_diUfcFyC8gAHhR3iBzYmFZPet6Z7x_L9JQenO2Z7iS-pp-pYN736zfgqP4PWH9u8VnXGY7gXXfl7SAfahjHRCmbio.4PXusQvBYMx8Sqd7siRGcU5__izjbFTFTAXjQpz4Wao&dib_tag=se&keywords=data+nerd+tshirt&qid=1720464589&sr=8-7'

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}


    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")

    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id='productTitle').get_text()

    price = soup2.find("span", class_="a-offscreen").get_text()

    price = price.strip()[1:]
    title = title.strip()

    today = datetime.date.today()
     

    data = [title, price, today]
    header = ['Title', 'Price', 'Date']

    with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        if os.path.getsize("AmazonWebScraperDataset.csv") > 0:
            writer.writerow(data)
        else:
            writer.writerow(header)
            writer.writerow(data)

    if(price < 14):
        send_mail()

def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    #server.starttls()
    server.ehlo()
    server.login('akay41024@gmail.com',f'{password}')
    
    subject = "The Shirt you want is below $14! Now is your chance to buy!"
    body = "Alex, This is the moment we have been waiting for. Now is your chance to pick up the shirt of your dreams. Don't mess it up! Link here: https://www.amazon.com/Data-Science-Programming-Programmer-T-Shirt/dp/B0C1TGFN8M/ref=sr_1_7?crid=2QDSC0MU1AFTY&dib=eyJ2IjoiMSJ9.8S8PRbJgIywHwKobIPqKaIAaiMGQQMpyI5OaQ8p_51uSrreRLr-mIf6Zj04R12ZB3a6PTzXNlNz41aQEirjbEcyvkQ3NiKjiYl8cFrHUF144VOSS7iaANP_zVjTHDZbOqV5k1ZI-OLTgfBwBUSZXv8ULObcfXnKLqWoWTtxHBgqIm85WMZ-0QD6sI2jUDmImRQTob8A274xiFsS7e_diUfcFyC8gAHhR3iBzYmFZPet6Z7x_L9JQenO2Z7iS-pp-pYN736zfgqP4PWH9u8VnXGY7gXXfl7SAfahjHRCmbio.4PXusQvBYMx8Sqd7siRGcU5__izjbFTFTAXjQpz4Wao&dib_tag=se&keywords=data+nerd+tshirt&qid=1720464589&sr=8-7"
   
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail(
        'asifkhan41024@gmail.com',
        msg
     
    )

while(True):
    check_price()
    time.sleep(5)
    df = pd.read_csv("AmazonWebScraperDataset.csv")
    print(df)
    