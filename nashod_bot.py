import requests, os
import sqlite3 as sl
from jdatetime import date , datetime
from pytz import timezone

DEBUG = False
if DEBUG:
    TOKEN = "2101502316:AAFtGv8QPxpHylBrOHQowzHa0zhpoXrnh3I"
    URL = "https://api.telegram.org/bot2101502316:AAFtGv8QPxpHylBrOHQowzHa0zhpoXrnh3I/"
else:
    TOKEN = "2128445444:AAEjn3_ASa8nUITT4r5wYpsnjmhtFCuECwc"
    URL = "https://api.telegram.org/bot2128445444:AAEjn3_ASa8nUITT4r5wYpsnjmhtFCuECwc/"

empty_profile_photo_id = "AgACAgQAAxkBAAICZ2GQz1n_OvY3ulMLRzv1UftfD5sNAAJBuDEbHf-BUMQvRPwwXgHdAQADAgADcwADIgQ"
commands = {"sabt_karhayee_ke_nakardam","نوشتن چیزی که نشد انجام بدم 📝","/listt", "کارهایی که بقیه انجام ندادن 🙋🏻‍♂️","/profile" ,"پروفایل 🙋🏼‍♀️🙋🏻‍♂️","/karbaran", "کاربران👨🏻‍💼👩🏻‍💼","/about", "درباره ما 📔","/home", "خانه🏠","/help", "راهنما ⛑"}

database_lacation1 = str(os.path.abspath(__file__))
database_lacation = database_lacation1[:-2] + "db"
users = {}
update_id = 0
update_id_new = 0
react = dict()
react1 = dict()
react2 = dict() #list safhe , messageid pm karha
react3 = dict() #pm direct, azin chiza
tarikh = list()
echoo = dict() #for chat


def send_url(url):
    #print(url)
    response = requests.get(url)
    return response.json()

def json_from_url(url):
    getUpdates = send_url(url)
    return getUpdates

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = json_from_url(url)
    return js

def get_last_update_id(updates): # vase ofsset
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def check_database():
    #print(os.path.abspath(database_lacation))
    return os.path.exists(database_lacation)

def create_database():
    con = sl.connect(str(database_lacation))
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE users (
    chat_id INTEGER,
    first_name TEXT,
    username TEXT,
    sex TEXT,
    profile_picture_id TEXT,
    bio TEXT,
    person_id2 TEXT,
    city TEXT,
    age INTEGER,
    last_online INTEGER,
    person_vasl INTEGER
        );
    """)

    cur.execute("""
        CREATE TABLE list (
    chat_id INTEGER,
    first_name TEXT,
    text_mext TEXT,
    number INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER
        );
    """)
    
    cur.execute("""
        CREATE TABLE messages (
    chat_id INTEGER,
    text_mext TEXT,
    number INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    photo_id = TEXT
        );
    """)

    con.commit()
    con.close()

def introduce_to_database(chat_id , username):
    name = str(users[chat_id]["first_name"])
    con = sl.connect(str(database_lacation))
    cur = con.cursor()
    query = "INSERT INTO users (chat_id, first_name, username) VALUES ({},\"{}\",\"{}\")".format(chat_id, name, username)
    #print("\n\n", query, "\n\n")
    cur.execute(query)
    con.commit()
    con.close()

# key3 is for list number
def write_in_database(key, key2, chat_id, first_name="", number=None):
    con = sl.connect(str(database_lacation))
    cur = con.cursor()
    if key == "first_name":
        query = "UPDATE users SET first_name = \"{}\" WHERE chat_id = {}".format(key2, chat_id)
        query1 = "UPDATE list SET first_name = \"{}\" WHERE chat_id = {}".format(key2, chat_id)
        cur.execute(query1)
    elif key == "sex":
        query = "UPDATE users SET sex = \"{}\" WHERE chat_id = {}".format(key2, chat_id)
    elif key == "profile_picture_id":
        query = "UPDATE users SET profile_picture_id = \"{}\" WHERE chat_id = {}".format(key2, chat_id)
    elif key == "bio":
        query = "UPDATE users SET bio = \"{}\" WHERE chat_id = {}".format(key2, chat_id)
    elif key == "list":
        query = "INSERT INTO list (chat_id, first_name, text_mext, number, year, month, day) VALUES ({},\"{}\",\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")".format(chat_id, first_name, key2, number, tarikh[0], tarikh[1], tarikh[2])
    elif key == "city":
        query = "UPDATE users SET city = \"{}\" WHERE chat_id = {}".format(key2, chat_id)
    elif key == "first_name_for_users":
        query = "UPDATE list SET first_name = \"{}\" WHERE chat_id = {}".format(key2, chat_id)
    elif key == "person_id2":
        query = "UPDATE users SET \"person_id2\"=\"{}\" WHERE chat_id = {}".format(key2, chat_id)
    elif key == "age":
        query = "UPDATE users SET age = \"{}\" WHERE chat_id = {}".format(key2, chat_id)
    elif key == "last_online":
        query = "UPDATE users SET \"last_online\" = \"{}\" WHERE chat_id = {}".format(key2, chat_id)
    elif key == "person_vasl":
        query = "UPDATE users SET \"person_vasl\" = \"{}\" WHERE chat_id = {}".format(key2, chat_id)
    elif key == "data_text":
        query = "INSERT INTO messages (chat_id, text_mext, year, month, day, person_id2) VALUES ({},\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")".format(chat_id, key2, tarikh[0], tarikh[1], tarikh[2],first_name)
    elif key == "data_photo":
        query = "INSERT INTO messages (chat_id, photo_id, year, month, day, person_id2) VALUES ({},\"{}\",\"{}\",\"{}\",\"{}\",\"{}\")".format(chat_id, key2, tarikh[0], tarikh[1], tarikh[2],first_name)
            
    #print("\n\n", query, "\n\n")
    cur.execute(query)
    con.commit()
    con.close()




#(number) is something for specify doing special work in this function
#number 1 is for all chat_id
#number 2 is for profile
#number 3 is for Null check
#number 4 is for read baghie anjamnadadn kar
#number 5 is for last list number
#number 6 is for cht_id from users
#number 7 is for chat_id to person_id2
def read_database(number,id_person ,marhale3=None, shomare=1): #shomare hamoon shomare safhe
    #print("we are connected to database telegram")
    con = sl.connect(str(database_lacation))
    cur = con.cursor()
    if number == 1:
        query = "SELECT chat_id FROM users"
        type(cur.execute(query))
        for chat_id in cur.execute(query):
            if id_person in chat_id:
                return True #hast
        return False

    elif number == 2:
        first_name=sex=profile_photo_id=bio=person_id2=city=age=None
        query = "SELECT * from users WHERE chat_id = {}".format(id_person)
        for x in cur.execute(query):
            #print(x)
            for column_number in range(1, 9):
                if column_number==1: first_name = x[column_number]
                elif column_number==3:
                    if x[column_number] == "m":
                        sex = "آقا🙋🏻‍♂️"
                    elif x[column_number] == "w":
                        sex = "خانم🙋🏻‍♀️"
                    else:
                        sex = x[column_number]
                elif column_number==4: profile_photo_id = x[column_number]
                elif column_number==5: bio = x[column_number]
                elif column_number==6: person_id2 = x[column_number]
                elif column_number==7: city = x[column_number]
                elif column_number==8: age = x[column_number]
        return first_name,sex,profile_photo_id,bio,person_id2,city,age

    elif number == 3:
        query = "SELECT {} FROM users WHERE chat_id = {}".format(marhale3, id_person)
        for x in cur.execute(query):
            if x[0] == None:
                return True
            else:
                return x[0]

    elif number ==4:
        if shomare ==0:
            return ""
        elif shomare == 1:
            start=0
            end=8
        else:
            #print("this is shomare: %i"%shomare)
            start=(shomare-1)*8
            end=start+8
        text = str()
        count = 0
        #print(marhale3)
        query = "SELECT * FROM list WHERE day={}".format(marhale3)
        #print("\n\n\n\n",query,"\n\n\n\n")
        for a in cur.execute(query):
            if start == count:
                username = read_database(7, a[0])
                text += "نام: " + a[1] + "%0A" + "آیدی: " +" /{}".format(username)+ "%0A" + a[2] + "%0A%0A"
                start += 1
            count += 1
            if count==end:
                break
        return text

    elif number ==5:
        num = int()
        count = 0
        query = "SELECT number FROM list WHERE day={}".format(marhale3)
        for a in cur.execute(query):
            #print(a)
            count += 1
        num = count

        #tedad_safhe = (int(num/8) + 1)
        return num

    elif number ==6:
        query = "SELECT chat_id FROM users"
        chat_ids = list()
        for a in cur.execute(query):
            chat_ids.append(a[0])
        return chat_ids

    elif number ==7:
        query = "SELECT person_id2 FROM users WHERE chat_id={}".format(id_person)
        for a in cur.execute(query):
            return a[0]

    elif number ==8:
        query = "SELECT person_id2 FROM users WHERE sex=\"{}\"".format(marhale3)
        #print("\n\n\n\n",query,"\n\n\n\n")
        last = ""
        for a in cur.execute(query):
            if a[0] != None:
                last = a[0]
        #print("this is last: ",last)
        return str(last)

    elif number ==9:
        query = "SELECT chat_id FROM users WHERE \"person_id2\"=\"{}\"".format(marhale3)
        for a in cur.execute(query):
            return a[0]

    elif number ==10:
        if shomare ==0:
            return ""
        elif shomare == 1:
            start=0
            end=8
        else:
            #print("this is shomare: %i"%shomare)
            start=(shomare-1)*8
            end=start+8
        text = str()
        count = 0
        #print(marhale3)
        query = "SELECT * FROM users"
        #print("\n\n\n\n",query,"\n\n\n\n")
        for a in cur.execute(query):
            if start == count:
                text += "نام: " + a[1] + "%0A" + "آیدی: " +" /{}".format(a[6])+ "%0A〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️%0A"
                start += 1
            count += 1
            if count==end:
                break
        return text
    
    elif number==11:
        query = "SELECT * FROM users WHERE \"chat_id\"=\"{}\"".format(id_person)
        for a in cur.execute(query):
            return a[6],a[1]
    
    elif number==12:
        id1 = dict()       
        query = "SELECT \"chat_id\",\"person_vasl\" FROM users where \"person_vasl\"!=\"\""
        for a in cur.execute(query):
            id1[a[0]] = a[1]
        return id1

    con.close()

def userid(getUpdates, i, chat_id):
    users[chat_id] = {}
    users[chat_id]["first_name"] = str(getUpdates["result"][i]["message"]["from"]["first_name"])
    username = "NULL"

    try: username = str(getUpdates["result"][i]["message"]["from"]["username"])
    except: None

    #print(users)
    introduce_to_database(chat_id, username)


def identify_person(getUpdates, chat_id, i):
    if read_database(1, chat_id) == False:
        userid(getUpdates, i, chat_id)
        return False
    else:
        return True

def identify_text(getUpdates):
    len_result = len(getUpdates["result"])
    text = ""
    photo_id = ""
    for i in range(len_result):

        if getUpdates["result"][i].get("my_chat_member") != None:
        #chat_id = getUpdates["result"][i]["my_chat_member"]["chat"]["from"]["id"]
        #name = getUpdates["result"][i]["my_chat_member"]["chat"]["from"]["first_name"
            if getUpdates["result"][i]["my_chat_member"]["new_chat_member"]["status"] == "kicked" or getUpdates["result"][i]["my_chat_member"]["old_chat_member"]["status"] == "kicked":
                pass
        elif getUpdates["result"][i].get("message") != None:
            try:
                text = getUpdates["result"][i]["message"]["text"]
            except:
                None
            try:
                caption = getUpdates["result"][i]["message"]["caption"]
            except:
                None
            try:
                photo_id = getUpdates["result"][i]["message"]["photo"][0]["file_id"]
                #print("\n\n\n\n\n",photo_id,"\n\n\n\n\n")
            except:
                None
            chat_id = getUpdates["result"][i]["message"]["from"]["id"]
            name = getUpdates["result"][i]["message"]["from"]["first_name"]

            identify = identify_person(getUpdates, chat_id, i)

            if (chat_id in react) and (text in commands):
                del react[chat_id]
            if (chat_id in react1) and (text in commands):
                del react1[chat_id]
            if (chat_id in react3) and (text in commands):
                del react3[chat_id]

            if text=="/start":
                if identify == False:
                    start_new_person(chat_id, name)
                elif identify == True:
                    start(chat_id, name, text)
            elif text in {"/sabt_nashod", "نوشتن چیزی که نشد انجام بدم 📝"}:
                sabt_karhayee_ke_nakardam(chat_id)
            elif text in {"/list_baghie", "کارهایی که بقیه انجام ندادن 🙋🏻‍♂️"}:
                listt(chat_id)
            elif text in {"/profile" ,"پروفایل 🙋🏼‍♀️🙋🏻‍♂️"}:
                profile(chat_id)
            elif text in {"/karbaran", "کاربران👨🏻‍💼👩🏻‍💼"}:
                karbaran(chat_id)
            elif text in {"/about", "درباره ما📔"}:
                about(chat_id)
            elif text in {"/home", "خانه🏠"}:
                start(chat_id, name, "((خانه🏠))")
            elif text in {"/help", "راهنما⛑"}:
                help(chat_id)
            elif text == "اتمام چت 🔙":               
               text = "- میخوای چت رو قطع کنی؟ 🌘 %0A- اگه اره ؛ %0A- دکمه ((❌❌❌)) بزن"
               url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text) + """&reply_markup={"inline_keyboard": [[{"text": "❌❌❌", "callback_data": "❌❌❌"}]]}"""
               send_url(url)
            elif text == "پروفایل کاربر 🙋🏻‍♂️":               
                profile(echoo[chat_id], chat_id, True)
            elif text == "/None":
                text1 = "پروفایل فرد مورد نظر هنوز تکمیل نشده است! 🦚"
                send_message(text1, chat_id)
            elif text.startswith("/boy") or text.startswith("/girl"):
                chat_id2 = read_database(9,None,text[1:])
                if chat_id2 == None:
                    text4 = "پروفایل مورد نظر وجود ندارد! 🦚"
                    send_message(text4, chat_id)
                else:
                    profile(chat_id2, chat_id)

            elif chat_id in react :
                change_person_Specifications(chat_id, text, photo_id)
                if react[chat_id] != "۱تغییر جنسیت":
                    del react[chat_id]
            elif chat_id in react1:
                if text == "ثبت ✅":
                    if react1[chat_id][0] == "":
                        text = "هیچ نوشته ای هنوز ارسال نکرده اید! ❌"
                        send_message(text, chat_id)
                    else:
                        number = read_database(5, chat_id, tarikh[2])
                        write_in_database("list", react1[chat_id][0], chat_id, name, number)
                        text = "خوب اوکی ؛ نوشته شما ثبت شد! ✅"
                        url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text) + """&reply_markup={"keyboard": [["نوشتن چیزی که نشد انجام بدم 📝"],["کارهایی که بقیه انجام ندادن 🙋🏻‍♂️"],["پروفایل 🙋🏼‍♀️🙋🏻‍♂️","کاربران👨🏻‍💼👩🏻‍💼"],["درباره ما📔","خانه🏠","راهنما⛑"]], "resize_keyboard":true}"""
                        send_url(url)
                        del react1[chat_id]
                elif text == "CANCEL ❌":
                    text = "نوشته شما ثبت نشد! ❌"
                    url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text) + """&reply_markup={"keyboard": [["نوشتن چیزی که نشد انجام بدم 📝"],["کارهایی که بقیه انجام ندادن 🙋🏻‍♂️"],["پروفایل 🙋🏼‍♀️🙋🏻‍♂️","کاربران👨🏻‍💼👩🏻‍💼"],["درباره ما📔","خانه🏠","راهنما⛑"]], "resize_keyboard":true}"""
                    send_url(url)
                    del react1[chat_id]
                else:
                    sabt_karhayee_ke_nakardam2(chat_id, None, text)
            
            elif chat_id in react3:
                if react3[chat_id].startswith("mail_"):    
                    text1 = "🪁آیا میخواین این پی ام رو ارسال کنم ؟%0A 🪁متن شما: %0A {}".format(text)
                    url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text1) + """&reply_markup={"inline_keyboard": [[{"text": "ارسال ☕️", "callback_data": "ارسال"},{"text": "🕳 لغو", "callback_data": "لغو"}]]}"""
                    send_url(url)
                    react3[chat_id] = [react3[chat_id],text]
            
            elif chat_id in echoo:
                if photo_id == "":
                    echo(chat_id, text)
                else:
                    echo(chat_id, None, photo_id)
                
                
            else:
                #print(echoo)
                namaloom(chat_id)

        elif getUpdates["result"][i].get("edited_message") != None:
            pass
        else:
            try:
                text = getUpdates["result"][i]["callback_query"]["message"]["text"]
            except:
                None
            chat_id = getUpdates["result"][i]["callback_query"]["from"]["id"]
            callback_data = getUpdates["result"][i]["callback_query"]['data']
            message_id = getUpdates["result"][i]["callback_query"]["message"]["message_id"]

            if callback_data == "ویرایش اطلاعات پروفایل":
                editMessageReplyMarkup_profile(chat_id, message_id)

            if callback_data in {"صفحه بعد","صفحه قبل","روز بعد","روز قبل"}:
                if chat_id not in react2:
                    break
                adad = int()
                if callback_data == "صفحه بعد":
                    adad = react2[chat_id][1] + 1
                    #print (adad)
                    rooz = react2[chat_id][2]
                    text1 = read_database(4,chat_id,rooz, adad)
                    if text1 == "":
                        text1 = "صفحه بعد وجود ندارد! 🦚"
                        send_message(text1, chat_id)
                    else:
                        listt2(text1, chat_id)
                        react2[chat_id][1] += 1
                elif callback_data == "صفحه قبل":
                    adad = react2[chat_id][1] - 1
                    #print (adad)
                    rooz = react2[chat_id][2]
                    text1 = read_database(4,chat_id,rooz, adad)
                    if text1 == "":
                        text1 = "صفحه قبل وجود ندارد! 🦚"
                        send_message(text1, chat_id)
                    else:
                        listt2(text1, chat_id)
                        react2[chat_id][1] -= 1

                elif callback_data == "روز قبل":
                    rooz = (react2[chat_id][2] - 1)
                    #print(rooz, type(rooz))

                    text1 = read_database(4,chat_id,rooz)
                    listt2(text1, chat_id, rooz)
                    react2[chat_id][2] -= 1
                elif callback_data == "روز بعد":
                    rooz = (react2[chat_id][2] + 1)
                    if rooz > tarikh[2]:
                        text1 = "فردا که وجود نداره! 🦚"
                        send_message(text1, chat_id)
                    else:
                        text1 = read_database(4,chat_id,rooz)
                        listt2(text1, chat_id, rooz)
                        react2[chat_id][2] += 1


            # ,"","","",""
            elif callback_data.startswith("chat_") or callback_data.startswith("mail_"):
                call = callback_data.split("_")
                name = call[4]
                person_id2 = call[2]+"_"+call[3]
                if callback_data.startswith("chat_"):
                    person_id,name1 = read_database(11,chat_id)
                    text = "- خوب من درخواست چت شما رو  برای کاربر /{} فرستادم! 😊%0A- هروقت  (( {} ))  آنلاین بشه ؛%0A-  درخواست چت شمارو میبینه ".format(person_id2, name)
                    send_message(text, chat_id)
                    text1 = "- سلااااام {}🤓%0A- همین الانِ‌ الان کابر /{}😄؛ %0A- درخواست چت با شمارو فرستاد.%0A- چت با این کاربر رو قبول میکنید؟ اگر بله!!!‌%0A- پس گزینه قبول درخواست رو انتخاب کنید.(چت با ایشان شروع میشه)".format(name,person_id)
                    url = URL + "sendMessage?chat_id=%s&text=%s"%(call[1], text1) + """&reply_markup={"inline_keyboard": [[{"text": "قبول درخواست ☕️", "callback_data": "connect_%i"}]]}"""%chat_id
                    send_url(url)
                    
                else:
                    io = callback_data.split("_")                   
                    text = "- پیامی که میخوای بفرستی برای%0A- کاربر: /{} %0A- پایین بنویس 👇🏻".format(io[2]+"_"+io[3])
                    send_message(text, chat_id)
                    react3[chat_id] = callback_data
                    
            elif callback_data in {"ارسال","لغو"}:
                if callback_data == "ارسال" and chat_id in react3:
                    text = "پی ام شما رو خیلی تند و سریع برای کابری که گفتین ارسال کردم ✅"
                    send_message(text , chat_id)    
                    io = react3[chat_id][0].split("_") 
                    person_id2,name = io[1],io[4]
                    person_id,name1 = read_database(11,chat_id)
                    text1 = "👤کاربر /{} برای شما این پی ام رو همین الان فرستاد:%0A〽️ متن پی ام: %0A(({})) ".format(person_id,react3[chat_id][1])
                    url = URL + "sendMessage?chat_id={}&text={}".format(person_id2,text1) + """&reply_markup={"inline_keyboard": [[{"text": "درخواست چت🎴", "callback_data": "chat_%i_%s_%s"},{"text": "🎴pm ارسال", "callback_data": "mail_%i_%s_%s"}]]}"""%(chat_id,person_id,name1,chat_id,person_id,name1) 
                    send_url(url)
                    del react3[chat_id]
                else:
                    text="پی ام شما رو ارسال نکردم ❌"
                    send_message(text, chat_id)
                    del react3[chat_id]
                
            
            elif callback_data in {"ورزش نکردن🏌️‍♂️","درس نخوندن📚","پاسخ ندادن ایمیل","ننوشتن پایان نامه","ماشین نشستن🚗"}:
                sabt_karhayee_ke_nakardam2(chat_id, callback_data)

            #shoro taghir profile
            elif callback_data in ["تغییر نام","تغییر جنسیت","تغییر بیو","تغییر عکس","تغییر شهر","۱تغییر جنسیت","تغییر سن"]:
                if callback_data == "تغییر نام":
                    text = "خیلی خوب ؛‌ اسم جدیدت رو این پایین بنویس : 👇🏻"
                    react[chat_id] = callback_data
                    send_message(text, chat_id)
                elif callback_data == "تغییر جنسیت":
                    text = "خوب حالا جنسیت خودت رو انتخاب کن:👇🏻"
                    react[chat_id] = callback_data
                    keyboard = """&reply_markup={"inline_keyboard": [[{"text": "آقا🙋🏻‍♂️", "callback_data": "m"},{"text": "خانم🙋🏻‍♀️", "callback_data": "w"}]]}"""
                    send_message(text, chat_id, keyboard)
                elif callback_data == "تغییر بیو":
                    text = "بیوی جدیدت رو برای من بنویس:👇🏻"
                    react[chat_id] = callback_data
                    send_message(text, chat_id)
                elif callback_data == "تغییر عکس":
                    text = "عکست جدید پروفایلت رو همین پایین بفرست:👇🏻"
                    react[chat_id] = callback_data
                    send_message(text, chat_id)
                elif callback_data == "تغییر شهر":
                    text = "نام شهرت رو همین پایین بنویس:👇🏻"
                    react[chat_id] = callback_data
                    send_message(text, chat_id)
                elif callback_data == "تغییر سن":
                    text = "سن خودت رو برای من بنویس:👇🏻"
                    react[chat_id] = callback_data
                    send_message(text, chat_id)

            elif callback_data.startswith("connect"):
                #print("\n\n\n\ni am here\n\n\n\n")
                id_2 = callback_data.split("_")
                echoo[chat_id]= int(id_2[1])
                echoo[int(id_2[1])]= chat_id
                #print("\n\n\n\n",echoo,"\n\n\n\n")
                #print("\n\n\n\n",id_2,"\n\n\n\n")
                
                person,name = read_database(11,chat_id)
                text = "🎈چت شما با کاربر /{} شروع شد🎈%0Aبا سلاااام ؛ صحبت خودت رو آغاز کن!".format(person)
                url = URL + "sendMessage?chat_id=%s&text=%s"%(id_2[1], text) + """&reply_markup={"keyboard": [["پروفایل کاربر 🙋🏻‍♂️"],["اتمام چت 🔙"]], "resize_keyboard":true}"""
                send_url(url)
                write_in_database("person_vasl", chat_id, int(id_2[1]))                
                
                person1, name1 = read_database(11,id_2[1])                
                text1 = "🎈چت شما با کاربر /{} شروع شد🎈%0Aبا سلاااام ؛ صحبت خودت رو آغاز کن!".format(person1)
                url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text1) + """&reply_markup={"keyboard": [["پروفایل کاربر 🙋🏻‍♂️"],["اتمام چت 🔙"]], "resize_keyboard":true}"""
                send_url(url)
                write_in_database("person_vasl",int(id_2[1]), chat_id)
                
                
            elif callback_data == "❌❌❌":
                text = "- چت شما همین الان به پایان رسید🚩%0A- صدقلاه علی و عظیم 🚩"
                url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text) + """&reply_markup={"keyboard": [["نوشتن چیزی که نشد انجام بدم 📝"],["کارهایی که بقیه انجام ندادن 🙋🏻‍♂️"],["پروفایل 🙋🏼‍♀️🙋🏻‍♂️","کاربران👨🏻‍💼👩🏻‍💼"],["درباره ما📔","خانه🏠","راهنما⛑"]], "resize_keyboard":true}"""
                send_url(url)               
                url = URL + "sendMessage?chat_id=%s&text=%s"%(echoo[chat_id], text) + """&reply_markup={"keyboard": [["نوشتن چیزی که نشد انجام بدم 📝"],["کارهایی که بقیه انجام ندادن 🙋🏻‍♂️"],["پروفایل 🙋🏼‍♀️🙋🏻‍♂️","کاربران👨🏻‍💼👩🏻‍💼"],["درباره ما📔","خانه🏠","راهنما⛑"]], "resize_keyboard":true}"""
                send_url(url)
                write_in_database("person_vasl","" ,chat_id)
                write_in_database("person_vasl","" ,int(echoo[chat_id]))                
                del echoo[echoo[chat_id]]
                del echoo[chat_id]
                              
                          
            elif chat_id in react:
                if react[chat_id] == "۱تغییر جنسیت":
                    change_person_Specifications(chat_id, text, photo_id, callback_data)
                else:
                    change_person_Specifications(chat_id, text, photo_id, callback_data)
                    del react[chat_id]



"""
        if chat_id == 171698111: #chat_id  mifo_support
            chat_id = 1438705092
        elif chat_id == 1438705092: #chat_id me
            chat_id = 171698111
        send_message(text, chat_id)
        """

def start_new_person(chat_id, name):
    text = "سلام {}! رفیق اینجا میتونی بنویسی امروز چه کار هایی رو انجام ندادی !".format(name)
    send_message(text, chat_id)
    text1 = "- برای کار با ربات ابتدا باید جنسیت خودتون را مشخص کنید: 👇🏻"
    keyboard = """&reply_markup={"inline_keyboard": [[{"text": "آقا🙋🏻‍♂️", "callback_data": "m"},{"text": "خانم🙋🏻‍♀️", "callback_data": "w"}]]}"""
    send_message(text1, chat_id, keyboard)
    react[chat_id] = "۱تغییر جنسیت"

def start(chat_id, name, command):
    text = "شما {} رو فرستادین 😅%0Aخوب من چکاری میتونم برات انجام بدم ؟%0A%0A- یکی از دکمه های پایین رو بزن 👇🏻".format(command)
    url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text) + """&reply_markup={"keyboard": [["نوشتن چیزی که نشد انجام بدم 📝"],["کارهایی که بقیه انجام ندادن 🙋🏻‍♂️"],["پروفایل 🙋🏼‍♀️🙋🏻‍♂️","کاربران👨🏻‍💼👩🏻‍💼"],["درباره ما📔","خانه🏠","راهنما⛑"]], "resize_keyboard":true}"""
    send_url(url)

def editMessageReplyMarkup_profile(chat_id, message_id):
    url = URL + "editMessageReplyMarkup?chat_id=%i&message_id=%i"%(chat_id, message_id,) + """&reply_markup={"inline_keyboard": [[{"text": "تغییر جنسیت 📝", "callback_data": "تغییر جنسیت"},{"text": "تغییر نام 📝", "callback_data": "تغییر نام"}],[{"text": "تغییر عکس 📝", "callback_data": "تغییر عکس"},{"text": "تغییر شهر 📝", "callback_data": "تغییر شهر"}],[{"text": "تغییر بیو📝", "callback_data": "تغییر بیو"},{"text": "تغییر سن 📝", "callback_data": "تغییر سن"}]]}"""
    send_url(url)

def change_person_Specifications(chat_id, text, photo_id=None, callback_data=None):
    if react[chat_id] == "تغییر نام":
        text2 = "نام تغییر نکرد ❌"
        if photo_id == None or callback_data == None:
            write_in_database("first_name", text, chat_id)
            text2 = "تغییرات ذخیره شد ✅"
            write_in_database("first_name_for_users", text, chat_id)
        send_message(text2, chat_id)
        profile(chat_id)
    elif react[chat_id]  == "تغییر عکس":
        text2 = "عکس تغییر نکرد ❌"
        if photo_id != "":
            write_in_database("profile_picture_id", photo_id, chat_id)
            text2 = "تغییرات ذخیره شد ✅"
        send_message(text2, chat_id)
        profile(chat_id)
    elif react[chat_id]  == "تغییر جنسیت":
        text2 = "جنسیت تغییر نکرد ❌"
        if callback_data != None:
            text2 = "تغییرات ذخیره شد ✅"
            if callback_data == "m":
                last_person_id = read_database(8,None,"m").split("_")
                #print(type(last_person_id), last_person_id)
                num = int(last_person_id[1]) +1
                new_id_person_2 = last_person_id[0] + "_" + '%05d' %num
                write_in_database("person_id2", new_id_person_2, chat_id)
            else:
                last_person_id = read_database(8,None,"w").split("_")
                num = int(last_person_id[1]) +1
                new_id_person_2 = last_person_id[0] + "_" + '%05d' %num
                write_in_database("person_id2", new_id_person_2, chat_id)
            write_in_database("sex", callback_data, chat_id)
        send_message(text2, chat_id)
        profile(chat_id)
    elif react[chat_id]  == "تغییر بیو":
        text2 = "بیو تغییر نکرد ❌"
        if photo_id == None or callback_data == None:
            write_in_database("bio", text, chat_id)
            text2 = "تغییرات ذخیره شد ✅"
        send_message(text2, chat_id)
        profile(chat_id)
    elif react[chat_id]  == "تغییر شهر":
        text2 = "شهر شما تغییر نکرد ❌"
        if react[chat_id] == "تغییر شهر":
            write_in_database("city", text, chat_id)
            text2 = "تغییرات ذخیره شد ✅"
        send_message(text2, chat_id)
        profile(chat_id)
    elif react[chat_id]  == "تغییر سن":
        text2 = "سن شما تغییر نکرد!❌"
        if react[chat_id] == "تغییر سن":
            write_in_database("age", int(text), chat_id)
            text2 = "تغییرات ذخیره شد ✅"
        send_message(text2, chat_id)
        profile(chat_id)    
    elif react[chat_id] == "۱تغییر جنسیت":
        text2 = "لطفا جنسیت خودتون رو انتخاب کنید! 🙋🏻‍♂️🙋🏼‍♀️"
        text = ""
        if callback_data != None:
            text2 = "جنسیت شما ذخیره شد ✅"
            send_message(text2, chat_id)
            if callback_data == "m":
                last_person_id = read_database(8,None,"m").split("_")
                #print(type(last_person_id), last_person_id)
                num = int(last_person_id[1]) +1
                new_id_person_2 = last_person_id[0] + "_" + '%05d' %num
                write_in_database("person_id2", new_id_person_2, chat_id)
            else:
                last_person_id = read_database(8,None,"w").split("_")
                num = int(last_person_id[1]) +1
                new_id_person_2 = last_person_id[0] + "_" + '%05d' %num
                write_in_database("person_id2", new_id_person_2, chat_id)
            write_in_database("sex", callback_data, chat_id)
            text = "یکی از دکمه های زیر رو انتخاب کن!"
            url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text) + """&reply_markup={"keyboard": [["نوشتن چیزی که نشد انجام بدم 📝"],["کارهایی که بقیه انجام ندادن 🙋🏻‍♂️"],["پروفایل 🙋🏼‍♀️🙋🏻‍♂️","کاربران👨🏻‍💼👩🏻‍💼"],["درباره ما📔","خانه🏠","راهنما⛑"]], "resize_keyboard":true}"""
            send_url(url)
            del react[chat_id]
        else:
            send_message(text2, chat_id)




def namaloom(chat_id):
    text = "ببین رفیق حقیقتش من این چیزی که تو میگی رو نمیفهمم! (اذیت نکن 😂)%0A%0A- اگه میخوای یکی از دکمه های پایین رو انتخاب کن: 👇🏻"
    url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text) + """&reply_markup={"keyboard": [["نوشتن چیزی که نشد انجام بدم 📝"],["کارهایی که بقیه انجام ندادن 🙋🏻‍♂️"],["پروفایل 🙋🏼‍♀️🙋🏻‍♂️","کاربران👨🏻‍💼👩🏻‍💼"],["درباره ما📔","خانه🏠","راهنما⛑"]], "resize_keyboard":true}"""
    send_url(url)

def profile(chat_id, chat_id2=None, re=None):
    #text = "این بخش درحال ساخت است"
    #send_message(text, chat_id)
    name = sex = bio = person_id2 = city = age = None
    name,sex,profile_photo_id,bio,person_id2,city,age = read_database(2, chat_id)
    if profile_photo_id == None:
        profile_photo_id = empty_profile_photo_id
    caption = "• نام: {} %0A• جنسیت: {}%0A• شهر: {} 🌆 %0A• سن: {}%0A%0A📋  بیو (bio): %0A {} %0A%0A🆔 آیدی: /{} %0A".format(name,sex,city,age,bio,person_id2)

    if chat_id2 == None and re == None:
        url = URL + "sendPhoto?chat_id={}&photo={}&caption={}".format(chat_id,profile_photo_id,caption) + """&reply_markup={"inline_keyboard": [[{"text": "ویرایش اطلاعات پروفایل✏️", "callback_data": "ویرایش اطلاعات پروفایل"}]]}"""
    elif chat_id2 != None and chat_id2 != chat_id and re == None:
        url = URL + "sendPhoto?chat_id={}&photo={}&caption={}".format(chat_id2,profile_photo_id,caption) + """&reply_markup={"inline_keyboard": [[{"text": "درخواست چت🎴", "callback_data": "chat_%i_%s_%s"},{"text": "🎴pm ارسال", "callback_data": "mail_%i_%s_%s"}]]}"""%(chat_id,person_id2,name,chat_id,person_id2,name)    
    elif chat_id2 != None and chat_id2 == chat_id and re == None:
        url = URL + "sendPhoto?chat_id={}&photo={}&caption={}".format(chat_id,profile_photo_id,caption) + """&reply_markup={"inline_keyboard": [[{"text": "ویرایش اطلاعات پروفایل✏️", "callback_data": "ویرایش اطلاعات پروفایل"}]]}"""
    elif chat_id2 != None and chat_id2 != chat_id and re == True:
        url = URL + "sendPhoto?chat_id={}&photo={}&caption={}".format(chat_id2,profile_photo_id,caption)
    send_url(url)

def sabt_karhayee_ke_nakardam(chat_id):
    text3 = "کار هایی که امروز انجام ندادین: 👇🏻%0A1) ...%0A2) ...%0A3) ...%0A4) ...%0A5) ...%0A."
    url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text3) + """&reply_markup={"inline_keyboard": [[{"text":"ورزش نکردن🏌️‍♂️", "callback_data": "ورزش نکردن🏌️‍♂️"},{"text": "درس نخوندن📚", "callback_data": "درس نخوندن📚"}],[{"text": "پاسخ ندادن ایمیل", "callback_data": "پاسخ ندادن ایمیل"},{"text": "ننوشتن پایان نامه", "callback_data": "ننوشتن پایان نامه"}],[{"text": "...", "callback_data": "..."},{"text": "ماشین نشستن🚗", "callback_data": "ماشین نشستن🚗"}]]}"""
    json = send_url(url)
    message_id = json["result"]["message_id"]

    text = "همچنین میتونی همین پایین تایپ کنی و بفرستی که چه کاری رو امروز نتونستی انجام بدی: 👇🏻"
    url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text) + """&reply_markup={"keyboard": [["ثبت ✅","CANCEL ❌"]], "resize_keyboard":true}"""
    send_url(url)

    react1[chat_id] = ["", message_id, 1, ""]

def sabt_karhayee_ke_nakardam2(chat_id, callback_data, text_r=""):
    if text_r != "":
        callback_data = text_r
    message_id = react1[chat_id][1]
    number = react1[chat_id][2]
    tarikh = str(date.today())
    react1[chat_id][3] = str(date.today())
    text = react1[chat_id][0]
    text += " - {}%0A".format(callback_data)
    text2 = "کار هایی که امروز انجام ندادین: 👇🏻%0A" + text
    url = URL + "editMessageText?chat_id=%i&message_id=%i&text=%s"%(chat_id, message_id, text2) + """&reply_markup={"inline_keyboard": [[{"text": "ورزش نکردن🏌️‍♂️", "callback_data": "ورزش نکردن🏌️‍♂️"},{"text": "درس نخوندن📚", "callback_data": "درس نخوندن📚"}],[{"text": "پاسخ ندادن ایمیل", "callback_data": "پاسخ ندادن ایمیل"},{"text": "ننوشتن پایان نامه", "callback_data": "ننوشتن پایان نامه"}],[{"text": "...", "callback_data": "..."},{"text": "ماشین نشستن🚗", "callback_data": "ماشین نشستن🚗"}]]}"""
    send_url(url)

    react1[chat_id][0] = text
    number += 1
    react1[chat_id][2] = number
    #print(react1)

def listt(chat_id):
    num = read_database(5,chat_id, tarikh[2])
    text3 = "🔆 نوشته های امروز  {}  تا می باشد 🔆".format(num)
    url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text3)
    json1 = send_url(url)
    message_id1 = json1["result"]["message_id"]
    if num == 0:
        text = "هیچ نوشته ای ؛ ثبت نشده! 📮"#.format("{}/{}/{}".format(tarikh[0],tarikh[1],tarikh[2]))
        url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text) + """&reply_markup={"inline_keyboard": [[{"text": "صفحه بعد🗂", "callback_data": "صفحه بعد"},{"text": "صفحه قبل🗂", "callback_data": "صفحه قبل"}],[{"text": "روز بعد📅", "callback_data": "روز بعد"},{"text": "روز قبل📅", "callback_data": "روز قبل"}]]}"""
    else:
        text = "خوب این ها کار هایی هستن که بقیه هم انجام ندادند: 👇🏻"
        send_message(text, chat_id)
        text1 = read_database(4, chat_id, tarikh[2]) #mahale3 inja tarikh rooz hast
        #if text1=="":
        #    text1 = "هیچی پیامی برای مشاهده  وجود ندارد"
        url = URL + "sendMessage?chat_id=%i&text=%s"%(chat_id, text1) + """&reply_markup={"inline_keyboard": [[{"text": "صفحه بعد🗂", "callback_data": "صفحه بعد"},{"text": "صفحه قبل🗂", "callback_data": "صفحه قبل"}],[{"text": "روز بعد📅", "callback_data": "روز بعد"},{"text": "روز قبل📅", "callback_data": "روز قبل"}]]}"""
    json = send_url(url)
    #print(json)
    message_id = json["result"]["message_id"]
    react2[chat_id] = [message_id, 1, tarikh[2], message_id1] #message_id

def listt2(text, chat_id ,rooz=None):
    if rooz != None:
        num = read_database(5,chat_id, rooz)
        text3 = "🔆 نوشته های  {} ⬅️ {}  تا می باشد 🔆".format("{}/{}/{}".format(tarikh[0],tarikh[1],rooz),num)
        if rooz == tarikh[2]:
            text3 = "🔆 نوشته های امروز  {}  تا می باشد 🔆".format(num)
        url = URL + "editMessageText?chat_id=%i&message_id=%i&text=%s"%(chat_id, react2[chat_id][3],text3) + """&reply_markup={"inline_keyboard": [[{"text": "صفحه بعد🗂", "callback_data": "صفحه بعد"},{"text": "صفحه قبل🗂", "callback_data": "صفحه قبل"}],[{"text": "روز بعد📅", "callback_data": "روز بعد"},{"text": "روز قبل📅", "callback_data": "روز قبل"}]]}"""
        send_url(url)

    if text == "":
        text = "هیچ نوشته ای {}ام ؛ ثبت نشده! 📮".format(rooz)
    message_id = react2[chat_id][0]
    url = URL + "editMessageText?chat_id=%i&message_id=%i&text=%s"%(chat_id, message_id,text) + """&reply_markup={"inline_keyboard": [[{"text": "صفحه بعد🗂", "callback_data": "صفحه بعد"},{"text": "صفحه قبل🗂", "callback_data": "صفحه قبل"}],[{"text": "روز بعد📅", "callback_data": "روز بعد"},{"text": "روز قبل📅", "callback_data": "روز قبل"}]]}"""
    send_url(url)


def karbaran(chat_id):
    text = read_database(10, None)
    #text = "این بخش در حال بروزرسانی می باشد!"
    send_message(text, chat_id)

def about(chat_id):
    text = " سلام 🛂%0A((نشد بات...☁️)) یه بخش از سرور (مهرشادینا)Ⓜ️%0Aاین ربات ربات یه ایده از یکی از دوستای مارتین بود و پاییز ۱۴۰۰ ساخته شد%0Aما همیشه آنلاین ؛ در دسترس شما هستیم😅"
    send_message(text, chat_id)

def help(chat_id):
    text = ("من اینجام که کمکت کنم!%0A برای دریافت راهنمایی در مورد هر موضوع، کافیه دستور آبی رنگی که مقابل اون سوال هست رو لمس کنی:%0A%0A👨‍💻 پشتیبانی ربات : %0A @Mehrshadina")
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    send_url(url)

def echo(chat_id, text=None, photo=None, voice=None, filee=None):    
    if text != None:
        send_message(text, echoo[chat_id])
        write_in_database("data_text", text, chat_id,echoo[chat_id])
    elif photo != None:
        url = URL + "sendPhoto?chat_id={}&photo={}".format(echoo[chat_id],photo) 
        send_url(url)
        write_in_database("data_photo", photo, chat_id,echoo[chat_id])
    elif voice != None:
        send_message(text, echoo[chat_id])
    elif filee != None:
        send_message(text, echoo[chat_id])
    #elif text != None:
        #send_message(text, echoo[chat_id])    
            

def send_message(text, chat_id, keyboard=""):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id) + keyboard
    send_url(url)

def edit_message(text1, chat_id, message_id):
    url = URL + "editMessageText?chat_id=%i&message_id=%i&text=%s"%(chat_id, message_id,text1)
    send_url(url)

def timee(key1):
    time = datetime.now(timezone("Asia/Tehran"))
    hour = time.hour
    minute = time.minute

    if key1 == 1:
        tarikh_1 = str(time.date()).split("-")
        tarikh.append(int(tarikh_1[0]))
        tarikh.append(int(tarikh_1[1]))
        tarikh.append(int(tarikh_1[2]))
        tarikh.append(False)
        print(tarikh)

    elif key1 == 2:
        if hour == 0 and minute == 0 :
            timee(1)
            date = str(time.date())
            today_name = time.strftime("%A")
            if today_name == "Saturday":
                today_name = "شنبه"
            elif today_name == "Sunday":
                today_name = "یک شنبه"
            elif today_name == "Monday":
                today_name = "دو شنبه"
            elif today_name == "Tuesday":
                today_name = "سه شنبه"
            elif today_name == "Wednesday":
                today_name = "چهار شنبه"
            elif today_name == "Thursday":
                today_name = "پنج شنبه"
            elif today_name == "Friday":
                today_name = "جمعه"
            if today_name == "یک شنبه":
                tarikh[3] = False
            angizeshi = "تو یه روز تو خیلی آدم موفقی میشی ، میدونستی من بهت ایمان دارم؟"
            text = "- شب بخیر دوست خوبم! 🌉%0A- هفته خیلی خوبی رو برای شما آرزو میکنم%0A- تاریخ:  {}  📅%0A- روز:  {}  📅%0A%0A(({}))".format(date,today_name, angizeshi)
            if today_name == "شنبه" and tarikh[3]==False :
                tarikh[3] = True
                chat_ids = read_database(6, None)
                for a in chat_ids:
                    #keyboard = """&reply_markup={"inline_keyboard": [[{"text": "جمله انگیزشی", "callback_data": "حمله انگیزشی"}]]}"""
                    send_message(text, a)

def babla_biar_echoo():
    id_ha = read_database(12, None)
    for a in id_ha:
        echoo[a] = id_ha[a]

def main():
    last_update_id = None
    if check_database() == False:
        create_database()
    timee(1)
    babla_biar_echoo()
    while True:
        timee(2)
        getUpdates = get_updates(last_update_id)
        if getUpdates is not None:
            if len(getUpdates["result"]) > 0:
                last_update_id = get_last_update_id(getUpdates) + 1
                identify_text(getUpdates)

if __name__ == '__main__':
    main()


#M09351045809
# send image
# https://api.telegram.org/bot1448655762:AAEMZcNYlPVe_X19rpVFo07yI4uIMYEeohU/sendPhoto?chat_id=171698111&photo=AgACAgQAAxkBAAIB02FUtdo7tfNzh8xJnN66G-wK5CeiAAJItjEbBfypUti9CnBFtnivAQADAgADcwADIQQ&caption=babe%0Ahey
#kik
"""{"ok":true,"result":[{"update_id":282136374,
"my_chat_member":{"chat":{"id":1778088991,"first_name":"Ali","username":"alirezaXsm","type":"private"},"from":{"id":1778088991,"is_bot":false,"first_name":"Ali","username":"alirezaXsm","language_code":"en"},"date":1635075474,"old_chat_member":{"user":{"id":1448655762,"is_bot":true,"first_name":"testone","username":"tanhaguitar_bot"},"status":"member"},"new_chat_member":{"user":{"id":1448655762,"is_bot":true,"first_name":"testone","username":"tanhaguitar_bot"},"status":"kicked","until_date":0}}},{"update_id":282136375,
"message":{"message_id":2613,"from":{"id":171698111,"is_bot":false,"first_name":"Mehrshad","username":"MifoSupport","language_code":"en"},"chat":{"id":171698111,"first_name":"Mehrshad","username":"MifoSupport","type":"private"},"date":1635075511,"text":"\u0633\u0641\u0627\u0631\u0634 \u0627\u0645\u062a\u062d\u0627\u0646 \u062c\u062f\u06cc\u062f \ud83d\udcdd"}}]}"""
#kik2
"""{"ok":true,"result":[{"update_id":282136376,
"my_chat_member":{"chat":{"id":1778088991,"first_name":"Ali","username":"alirezaXsm","type":"private"},"from":{"id":1778088991,"is_bot":false,"first_name":"Ali","username":"alirezaXsm","language_code":"en"},"date":1635076002,"old_chat_member":{"user":{"id":1448655762,"is_bot":true,"first_name":"testone","username":"tanhaguitar_bot"},"status":"kicked","until_date":0},"new_chat_member":{"user":{"id":1448655762,"is_bot":true,"first_name":"testone","username":"tanhaguitar_bot"},"status":"member"}}},{"update_id":282136377,
"message":{"message_id":2614,"from":{"id":1778088991,"is_bot":false,"first_name":"Ali","username":"alirezaXsm","language_code":"en"},"chat":{"id":1778088991,"first_name":"Ali","username":"alirezaXsm","type":"private"},"date":1635076007,"text":"/start","entities":[{"offset":0,"length":6,"type":"bot_command"}]}}]}"""

#CREATE TABLE users (chat_id INT, first_name VARCHAR(20), username VARCHAR(20), sex CHAR(1), profile_picture_id VARCHAR(90), dore_tahsili VARCHAR(20), marhale2_dore_tahsili VARCHAR(20),bio VARCHAR(500), person_id2 INT);
