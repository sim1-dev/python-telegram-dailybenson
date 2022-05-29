from random import randint
from pytube import YouTube
import os
from dotenv import load_dotenv, find_dotenv
import telebot
import schedule
import time
from time import sleep
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import logging
import datetime
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

# Init

load_dotenv(find_dotenv())

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

logging.basicConfig(filename=os.getenv('LOG_FILE'),
                    filemode='a',
                    format='%(levelname)s %(asctime)s - %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S',
                    level=logging.DEBUG)
log = logging.getLogger()

# Functions

def firstSetup():
    connection = sqlite3.connect(os.getenv('DB_NAME'))
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS chats (chat_id VARCHAR UNIQUE)")
    cursor.execute("CREATE TABLE IF NOT EXISTS links (url VARCHAR UNIQUE)")
    connection.commit()
    cursor.close()
    connection.close()

def mainSchedulerBenson():
    print('Starting scheduler...')
    while True:
        schedule.run_pending()
        time.sleep(60)

def botRunnerBenson():
    print('Starting bot...')
    try:
        bot.polling()
    except Exception as e:
        log.error(e)

def sendBensonClip():
    print('Sending clip...')
    try:
        videolength = 1501
        while(videolength > 1500):
            conn = sqlite3.connect(os.getenv('DB_NAME'))
            cursor = conn.cursor()
            cursor.execute("SELECT url FROM links ORDER BY RANDOM() LIMIT 1;")
            link = cursor.fetchone()[0]
            cursor.close()
            yt = YouTube(link)
            videolength = yt.length
            print(yt.title)
            sleep(1)
        start = randint(0, videolength - 30)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
        os.rename(yt.streams.first().default_filename.replace("3gpp", "mp4"), 'temp.mp4')
        ffmpeg_extract_subclip("temp.mp4", start, start + 30, targetname="clip.mp4")
        os.remove("temp.mp4")
        cursor = conn.cursor()
        cursor.execute("SELECT chat_id FROM chats")
        chats = cursor.fetchall()
        for chat in chats:
            try:
                bot.send_video(chat[0], video=open('clip.mp4', 'rb'), supports_streaming=True)
                bot.send_message(chat[0], yt.title)
            except Exception as e:
                log.error(e)
                pass
        os.remove("clip.mp4")
        conn.close()
    except:
        #print('streamingData error: try reinstalling pytube3 (https://github.com/pytube/pytube/issues/743)')
        sendBensonClip()

def run_io_tasks_in_parallel(tasks):
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()

def saveChatId(chatId):
    conn = sqlite3.connect(os.getenv('DB_NAME'))
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT OR IGNORE INTO chats (chat_id) VALUES (?)', (chatId,))
    except Exception as e:
        log.error(e)
    conn.commit()
    cursor.close()
    conn.close()

def deleteChatId(chatId):
    conn = sqlite3.connect(os.getenv('DB_NAME'))
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM chats WHERE chat_id=?', (chatId,))
    except Exception as e:
        log.error(e)
    conn.commit()
    cursor.close()
    conn.close()

# Scheduler

schedule.every().day.at("12:00").do(sendBensonClip)

# Start Logic

firstSetup()

log.info("BOT STARTED")

# Bot Commands

@bot.message_handler(commands=['attivarichard'])
def attivarichard(message):
    if(str(message.chat.type) != 'private'):
        userInGroupDetails = bot.get_chat_member(message.chat.id, message.from_user.id)
        log.info(userInGroupDetails)                                                                                                                            # Discussion Groups (Groups bound to a specific channel)
        if(str(os.getenv('OWNER_ID')) == str(message.from_user.id) or userInGroupDetails.status == 'administrator' or userInGroupDetails.status == 'creator' or userInGroupDetails.user.is_bot == True):
        #if(str(os.getenv('OWNER_ID')) == str(message.from_user.id)): # private bot
            try:
                saveChatId(str(message.chat.id))
                log.info("BOT ATTIVATO NEL GRUPPO "+ message.chat.title + " " + str(message.chat))
                finalMessage = "[OK] Richard Benson attivato nel gruppo " + message.chat.title
            except:
                finalMessage = "[ER] Bot già attivo nel gruppo"
        else:
            finalMessage = "[ER] Non sei autorizzato ad utilizzare questo comando."
        bot.send_message(message.chat.id, finalMessage)

@bot.message_handler(commands=['disattivarichard'])
def disattivarichard(message):
    if(str(message.chat.type) != 'private'):
        userInGroupDetails = bot.get_chat_member(message.chat.id, message.from_user.id)                   
        if(str(os.getenv('OWNER_ID')) == str(message.from_user.id) or userInGroupDetails.status == 'administrator' or userInGroupDetails.status == 'creator' or userInGroupDetails.user.is_bot == True):
        #if(str(os.getenv('OWNER_ID')) == str(message.from_user.id)): # private bot
            try:
                deleteChatId(str(message.chat.id))
                log.info("BOT DISATTIVATO NEL GRUPPO "+ message.chat.title + " " + str(message.chat))
                finalMessage = "[OK] Richard Benson disattivato nel gruppo " + message.chat.title
            except:
                finalMessage = "[ER] Bot non attivo nel gruppo"
        else:
            finalMessage = "[ER] Non sei autorizzato ad utilizzare questo comando."
        bot.send_message(message.chat.id, finalMessage)

@bot.message_handler(commands=['start'])
def start(message):
    if(str(message.chat.type) == 'private'):
        saveChatId(str(message.chat.id))
        bot.send_message(message.chat.id, "TI DEVI SPAVENTAREEEEEEEEEEEEEEEEEEEEEEEEEEEE")

@bot.message_handler(commands=['denow'])
def denow(message):
    bot.send_message(message.chat.id, str(datetime.datetime.now()))

@bot.message_handler(commands=['dona'])
def dona(message):
    target = message.chat.id
    if(str(message.chat.type) != 'private'):
        userInGroupDetails = bot.get_chat_member(message.chat.id, message.from_user.id)
        if(userInGroupDetails.user.is_bot != True):
            target = str(message.from_user.id)
    try:
        bot.send_message(target, "Ciao! Il Bot è totalmente gratuito e presto sarà anche Open Source, ma se proprio vuoi regalarmi un caffè clicca pure su questo link: https://www.paypal.com/donate/?hosted_button_id=ZK6C72K5BKQHA")
    except:
        bot.send_message(message.chat.id, "[ER] Per evitare spam questo comando può essere lanciato solo in privato.")

@bot.message_handler(commands=['test'])
def test(message):
    if(str(message.chat.type) == 'private'):
        if(str(os.getenv('OWNER_ID')) == str(message.from_user.id)):
            sendBensonClip()
            bot.send_message(message.chat.id, "Clip inviata!")

# Multithreading Logic

run_io_tasks_in_parallel([
    botRunnerBenson,
    mainSchedulerBenson,
])

