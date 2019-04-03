import JustIRC
import random
import requests
import re
import time

bot = JustIRC.IRCConnection()

greetings = [
    "Hello {}!",
    "Hi {}!",
    "Hello there {}!",
    "Hi there {}!",
    "Hey {}!"
]

def on_connect(bot):
    bot.set_nick("")
    bot.send_user_packet("")

def on_welcome(bot):
    bot.send_message('NickServ', 'identify ')
    print('Authed to NickServ')
    time.sleep(199)
    bot.join_channel('#wikipedia-en-appleinc')
    print('Joined w-e-ai')
    bot.join_channel('##test1')
    print('Joined #t1')
def on_message(bot, channel, sender, message):
    if "hi" == message.lower() or "hello" == message.lower():
        greeting_message = random.choice(greetings).format(sender)
        bot.send_message(channel, greeting_message)
    if '!status' == message.lower():
        bot.send_message(channel, 'Under Development'.format(sender))
    if message.split()[0] == "!weather":
        if len(message.split()) > 1:
            location = message.lower()
            location = location[9:]
            print(location)
            weather_data = requests.get("http://api.openweathermap.org/data/2.5/weather?q="+location+"&APPID=&units=metric").json()
            if weather_data["cod"] == 200:
                bot.send_message(channel, "The weather in {} is {} and {} degrees.".format(weather_data["name"], weather_data["weather"][0]["description"], weather_data["main"]["temp"]))
            else:
                bot.send_message('RhinosF1', 'API Fault')
        else:
            bot.send_message(channel, "Usage: !weather Istanbul")
    for message_part in message.split():
        if message_part.startswith("http://") or message_part.startswith("https://"):
            html = requests.get(message_part).text
            title_match = re.search("<title>(.*?)</title>", html)
            if title_match:
                bot.send_message(channel, "Title of the URL by {}: {}".format(sender, title_match.group(1)))
    for message_part in message.split():
        if message_part.startswith('!help'):
            bot.send_message(channel, "Welcome to #wikipedia-en-appleinc. Just ask away if you've got a question about anything apple-related or regarding the wikiproject. For general wikipedia assistance, you may get faster help in #wikipedia-en-help")
        elif message_part.startswith('!ops'):
            opcount = open('oplog.txt', 'r')
            opnum = opcount.read()
            opcount.close()
            opnum = int(opnum) + 1
            opcount = open('oplog.txt', 'w+')
            opcount.write(str(opnum))
            opcount.close()
            if opnum < 3:
                bot.send_message(channel, 'Operators have been notified. If no one responds, contact a freenode staff member in #freenode or a wmfgc.')
                bot.send_message('dtm', 'Operator assistance needed in #wikipedia-en-appleinc')
                bot.send_message('RhinosF1', 'Operator assistance needed in #wikipedia-en-appleinc')
                print('OP stalk was used.')
            if opnum == 3:
                bot.send_message(channel, 'If no operator is responding then contact a wmfgc or freenode staff member in #freenode.')
                bot.send_message('dtm',"Please assist in #wikipedia-en-appleinc - the user may now contact freenode staff or a wmfgc")
                bot.send_message('RhinosF1',"Please assist in #wikipedia-en-appleinc - the user may now contact freenode staff or a wmfgc")
                print('OP needed')
            if opnum > 3:
                bot.send_message(channel, 'Please contact a wmfgc or freenode staff member in #freenode. No chanops seem to responding')
                bot.send_message('', 'User requesting op assistance has been reffered to other assistance methods')
                bot.send_message('','User requesting op assistance has been reffered to other assistance methods')
                
    if 'block me' == message.lower():
        bot.send_message('ChanServ', 'op '+ channel + ' ')
        bot.send_line('KICK ' + channel + ' ' + sender + 'spam')
        bot.send_message(str(sender), 'You were kicked for spam from ' + channel)
        bot.send_message('ChanServ', 'deop ' + channel + ' ')
                          

bot.on_connect.append(on_connect)
bot.on_welcome.append(on_welcome)
bot.on_public_message.append(on_message)

bot.connect("chat.freenode.net")
bot.run_loop()
