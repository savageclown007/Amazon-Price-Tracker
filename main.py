import requests
from bs4 import BeautifulSoup
import smtplib
import tkinter
from tkinter import *
import time
from PIL import ImageTk, Image
from threading import *


class mainF(Thread):
    def run(self):
        URL=Url_Entry.get()
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}
        currPrice  = 0.00
        email_add=Email_Entry.get()
        
        def check(currPrice,URL,headers,email_add):

            page = requests.get(URL,headers=headers)

            soup=BeautifulSoup(page.content,'html.parser')

            title = soup.find(id='productTitle').get_text()
            title=title.strip()

            deal=soup.find(id='priceblock_ourprice')
            if deal==None:
                deal=soup.find(id='priceblock_dealprice')


            price = deal.get_text()[2:].split(',')

            priceF = ''
            for i in price:
                priceF+=i
        
            fprice = float(priceF)
            flag = False
            if fprice <= currPrice:
                currPrice = send_mail(URL,email_add,title)
            else:
                currPrice = fprice

            return currPrice

        def send_mail(URL,email_add,title):
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.ehlo()
            server.starttls()
            server.ehlo()

            server.login('trackeramazon35@gmail.com','Tracker@35')

            subject = 'Price fell down!'
            body = 'Check your product\n'+title+ '\n'+ URL

            msg = f"Subject: {subject}\n\n{body}"

            server.sendmail(
                'trackeramazon35@gmail.com',
                email_add,
                msg
            )
            

            server.quit()
            return -1   
        while True:
            currPrice=check(currPrice,URL,headers,email_add)
            if(currPrice==-1):
                break
                close_window() 
            time.sleep(10)     

        def close_window():
            top.quit()


def info():
    l2=Label(top,text="Your product is being tracked.We'll send an email as the price go down.", bg = '#7EC0EE', font=("Comic Sans MS",20))
    l2.place(relx = 0.18, rely = 0.7, relwidth = 0.70, relheight = 0.16)
    t1=mainF()
    t1.start()
  
    






top=tkinter.Tk()
top.geometry('1920x1080')
top.minsize(width = 400, height = 400)

background_image = Image.open("Back.jpg")

img = ImageTk.PhotoImage(background_image)

Canvas1 = Canvas(top)
Canvas1.create_image(300, 340, image = img)
Canvas1.pack(side = 'left', expand = True, fill = BOTH)

headingFrame1 = Frame(top, bg = "#5B59BA", bd = 5)                                                    #Frame
headingFrame1.place(relx = 0.18, rely = 0.1, relwidth = 0.70, relheight = 0.16)                   #frame config

#Heading portion
headingLabel1 = Label(headingFrame1, text = "Welcome to \n Amazon Price Tracker", bg = '#7EC0EE', fg = 'white', font = ('Showcard Gothic', 40))
headingLabel1.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

Url_Label = Label(top, text = "Enter the URL of product", bg = '#7EC0EE', fg = 'black', font=('Segoe Script', 16))
Url_Label.place(relx = 0.18, rely = 0.3, relwidth = 0.20, relheight = 0.1)
Url = StringVar()
Url_Entry = Entry(top, textvariable = Url, bg = '#BFEFFF', fg = 'black', font=('Comic Sans MS', 10))
Url_Entry.place(relx = 0.38, rely = 0.3, relwidth = 0.50, relheight = 0.1)

Email_Label = Label(top, text = "Enter your Email ID", bg = '#7EC0EE', fg = 'black', font=('Segoe Script', 16))
Email_Label.place(relx = 0.18, rely = 0.4, relwidth = 0.20, relheight = 0.1)
email = StringVar()
Email_Entry = Entry(top, textvariable = email, bg = '#BFEFFF', fg = 'black', font=('Comic Sans MS', 16))
Email_Entry.place(relx = 0.38, rely = 0.4, relwidth = 0.50, relheight = 0.1)

headingFrame2 = Frame(top, bg = "#5B59BA", bd = 5)                                                    #Frame
headingFrame2.place(relx = 0.40, rely = 0.55, relwidth = 0.20, relheight = 0.1)                   #frame config

b=Button(headingFrame2, text="Start Tracker",command = info, bg = '#7EC0EE', font = ('Comic Sans MS', 20))
b.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

top.mainloop()
