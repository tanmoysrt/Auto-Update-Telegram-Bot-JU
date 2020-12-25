import json
import psycopg2
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASS")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")

conn = psycopg2.connect(database=db_name, user = db_user, password = db_password, host = db_host, port = db_port)

# For HomePage Hash Retrieval & Update
def getCurrentHashOfJUHomePage():
    cur = conn.cursor()
    cur.execute("SELECT id, hash  from juhomepage")
    row = cur.fetchall()[0][1]
    return  row

def updateCurrentHashOfJUHomePage(newHash):
    try:
        cur = conn.cursor()
        cur.execute("UPDATE juhomepage set hash = (%s) where id = 1",(str(newHash),))
        conn.commit()
        return True
    except:
        return False

# To get all rows from Notice Links db
def getJuNoticeSectionsData():
    cur = conn.cursor()
    cur.execute("SELECT id, name, url,data,name_id  from ju_notice_section")
    conn.commit()
    row = cur.fetchall()
    return row


def getJuNoticeSectionsSelectedData(name_id):
    try:
        cur = conn.cursor()
        cur.execute("SELECT data from ju_notice_section where name_id = (%s)",(str(name_id),))
        conn.commit()
        row = json.loads(cur.fetchall()[0][0])
        return row
    except:
        conn.rollback()
        return []

# Update Data Of Notice Section in DB
def updateDataOfNoticeSection(data,name):
    try:
        cur = conn.cursor()
        data = json.dumps(data)
        cur.execute("UPDATE ju_notice_section set data = (%s) where name_id = (%s)",(data,name,))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

# Add new record to telegram groups database
def insertRecordTelegramGroup(chatid,name):
    try:
        currentdate = str(datetime.date.today().strftime("%d%m%Y"))
        cur = conn.cursor()
        cur.execute("SELECT id, chatid  from telegram_group where chatid=(%s)", (str(chatid),))
        if len(cur.fetchall()) > 0 :
            return True
        cur = conn.cursor()
        cur.execute("INSERT INTO telegram_group (name,created_at,chatid) \
                    VALUES ((%s),TO_DATE((%s),'DDMMYYYY'),(%s) )",(str(name),str(currentdate),str(chatid),))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

# Add new record to telegram users database
def insertRecordTelegramUser(chatid,name):
    try:
        currentdate = str(datetime.date.today().strftime("%d%m%Y"))
        cur = conn.cursor()
        cur.execute("SELECT id, chatid  from telegram_user where chatid=(%s)", (str(chatid),))
        if len(cur.fetchall()) > 0 :
            return True
        cur = conn.cursor()
        cur.execute("INSERT INTO telegram_user (name,created_at,chatid) \
                    VALUES ((%s),TO_DATE((%s),'DDMMYYYY'),(%s) )",(str(name),str(currentdate),str(chatid),))
        conn.commit()
        return True
    except Exception as e:
        print(e)
        conn.rollback()
        return False

# Add new record to email subscriptions database
def insertRecordEmailSubscriptions(name,emailid,chatid=""):
    try:
        currentdate = str(datetime.date.today().strftime("%d%m%Y"))
        cur = conn.cursor()
        cur.execute("SELECT id, email_id  from email_subscriptions where email_id=(%s)", (str(emailid),))
        if len(cur.fetchall()) > 0 :
            return True
        cur = conn.cursor()
        cur.execute("INSERT INTO email_subscriptions (name,created_at,telegram_id, email_id) \
                    VALUES ((%s),TO_DATE((%s),'DDMMYYYY'),(%s),(%s) )",(str(name),str(currentdate),str(chatid),str(emailid),))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

# Get list of telegram groups
def getTelegramGroups():
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, chatid  from telegram_group")
        rows=cur.fetchall()
        return rows
    except:
        conn.rollback()
        return []

# Get list of telegram users
def getTelegramUsers():
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, chatid  from telegram_user")
        rows=cur.fetchall()
        return rows
    except:
        conn.rollback()
        return []

# Get list of email subscribers
def getEmailSubscriptions():
    try:
        cur = conn.cursor()
        cur.execute("SELECT id, name, email_id,telegram_id  from email_subscriptions")
        rows=cur.fetchall()
        return rows
    except:
        conn.rollback()
        return []


