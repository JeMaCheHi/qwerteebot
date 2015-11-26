import telebot
from telebot import types
from bs4 import BeautifulSoup
import requests
import urllib
import time


TOKEN = '152117700:AAF9HtX6R9laqacmLi6gmL48Wq91BFFoRk4'

bot = telebot.TeleBot(TOKEN)

#################
#   Listener    #
#################

def listener(messages):
    for m in messages:
        cid = m.chat.id
        print ("[" + str(cid) + "]: " + m.text)
        
bot.set_update_listener(listener)

#################
#   Commands    #
#################

#help command
@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    helpstr = ( "I'm a cool bot that will show you the current offers from Qwertee."
                "List of commands:\n"
                "/today: Shows the tees selling today\n"
                "/lastchance: Shows the tees from yesterday, it's your last chance to get them!"
                
                "You can visit qwertee.com to see the whole list of tees :D"
    )
    bot.send_message(cid, helpstr)
    
    
#/today command
@bot.message_handler(commands=['today'])
def command_today(m):
    cid = m.chat.id #get chat ID so we can respond
    url = "http://www.qwertee.com"
    req = requests.get(url)
    statusCode = req.status_code
    if statusCode == 200:   #check if the web is up
        html = BeautifulSoup(req.text)
        divs = html.find_all("div", class_="tee-current")
        for sect in divs:
            pic = sect.find("img", class_="dynamic-image-design")['src']
            f = open("pic.png", "wb")
            #Since the pic is stored on a cdn.* url, we have to reformat it to use https
            f.write(urllib.request.urlopen("https://www." + pic[6:]).read())
            f.close()
            bot.send_photo(cid, open("pic.png","rb"))
    else:
        bot.send_message(cid, "Webpage error, try again later")
        
#lastchance command
@bot.message_handler(commands=['lastchance'])
def command_lastchance(m):
    cid = m.chat.id #get chat ID so we can respond
    url = "http://www.qwertee.com"
    req = requests.get(url)
    statusCode = req.status_code
    if statusCode == 200:   #check if the web is up
        html = BeautifulSoup(req.text)
        lastchance = html.find("div", id="last-chance-desktop")
        divs = lastchance.find_all("div", class_="inner")
        for sect in divs:
            pic = sect.find("img")['src']
            f = open("pic.jpg", "wb")
            #Since the pic is stored on a cdn.* url, we have to reformat it to use https
            f.write(urllib.request.urlopen("https://www." + pic[6:]).read())
            f.close()
            bot.send_photo(cid, open("pic.jpg","rb"))
    else:
        bot.send_message(cid, "Webpage error, try again later")
        
#auto command
@bot.message_handler(commands=['auto'])
def command_auto(m):
    cid = m.chat.id
    bot.send_message(cid, "Sorry, this feature is still unimplemented :'(")

bot.polling(none_stop=True) 
