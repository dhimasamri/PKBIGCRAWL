from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import random
import pandas as pd
import time
import selenium
import csv


# Atributtes ------------------------------------
driver = webdriver.Chrome(r"chromedriver.exe")
username = "Masukkan username disini"
password = "Masukkan password disini"
current_user = username
checkedList = []
datNum = 1
maxDat = 300000
set_delay = 5
fastView = True


# Fun Fun -------------------------------------------
def closeBrowser():
    driver.close()

def login():
    """
    fungsi untuk login pertama kali
    harap diperhatikan bahwa username dan password di set terlebih dahulu di bagian atribut diatas
    fungsi ini akan mengarahkan anda sampai ke halaman home user
    tidak menghasilkan return
    """
    
    driver.get("https://www.instagram.com/accounts/login/?hl=id&source=auth_switcher")
    time.sleep(set_delay)

    user_name_elem = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input""")
    user_name_elem.clear()
    user_name_elem.send_keys(username)

    passworword_elem = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input""")
    passworword_elem.clear()
    passworword_elem.send_keys(password)
    passworword_elem.send_keys(Keys.RETURN)
    time.sleep(set_delay)

    try:
        ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.HoLwm"))).click()
    finally:
        pass

    akun_elem = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/section/div[3]/div[1]/div/div[2]/div[1]/a""")
    akun_elem.click()

def loopPost(userName):
    """
    ini adalah fungsi untuk mengloop post
    setiap post yang di loop akan diambi username, caption, hastag, likes, dan comment
    fungsi ini membutuhkan fungsi-fungsi lain, yaitu:
        fungsi listFormat()
        fungsi getLikes()
        fungsi getCaption()
        fungsi getComment()
        fungsi getHastag()
        fungsi getAccount()
    secara otomatis akan menulis ke file csv
    tidak menghasilkan return
    """

    try:
        a = "https://www.instagram.com/" + userName
        driver.get(a)
        jumlahPost = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span""").text
        jumlahPost = int(jumlahPost)
    except:
        print("Akun mungkin di-PRIVATE")
        return
                        
    try:
        post1 = driver.find_element_by_class_name("_9AhH0")
        post1.click()
        time.sleep(set_delay)
        alist = listFormat()
        csvWriter(alist)
    except:
        print("Mungkin tidak ada post")
        return 

    try:
        Post2 = driver.find_element_by_class_name("HBoOv.coreSpriteRightPaginationArrow")
        Post2.click()
        time.sleep(set_delay)
        alist = listFormat()
        csvWriter(alist)
    except:
        print("tidak bisa next")
        return 

    for i in range(jumlahPost-2):
        try:
            nextPost = driver.find_element_by_class_name("HBoOv.coreSpriteRightPaginationArrow")
            nextPost.click()
            time.sleep(set_delay)
            alist = listFormat()
            csvWriter(alist)
            showCSVinPD("DataLevel1.csv")
        except:
            pass
    driver.get(a)

def getLikes(): # return number of likes
    """
    fungsi yang mereturn jumlah like dari suatu post
    fungsi dibuat untuk digunakan pada fungsi loopPost()
    return int
    """
    try:
        jmlLike = driver.find_element_by_xpath("""/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div[2]/button/span""").text
        return jmlLike
    except:
        try:
            jmlLike = driver.find_element_by_xpath("""/html/body/div[3]/div[2]/div/article/div[2]/section[2]/div/div/button/span""").text
            return jmlLike
        except:
            print("Like ERROR in post number ", datNum)
            return 0
    
def getCaption(): # return string of caption
    """
    fungsi yang mereturn Caption dari suatu post
    fungsi dibuat untuk digunakan pada fungsi loopPost()
    return string
    """
    try:
        Caption = driver.find_element_by_xpath("""/html/body/div[3]/div[2]/div/article/div[2]/div[1]/ul/div/li/div/div/div[2]/span""").text
        Caption = Caption.replace('\r', ' ').replace('\n', ' ')
        Caption = ''.join([i if ord(i) < 128 else ' ' for i in Caption])    # Remove non ASCII
        return Caption
    except:
        print("Caption ERROR in post number", datNum)
        Caption = " "
        return Caption

def getAccount(): # return string of account
    """
    fungsi yang mereturn account dari suatu post
    fungsi dibuat untuk digunakan pada fungsi loopPost()
    return string
    """
    try:
        Account = driver.find_element_by_xpath("""/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div/h2/a""").text
    except:
        Account = driver.find_element_by_xpath("""/html/body/div[3]/div[2]/div/article/header/div[2]/div[1]/div[1]/h2/a""").text
    return Account

def getHastag(): # return list of hastag
    """
    fungsi yang mereturn hastag dari suatu post
    fungsi dibuat untuk digunakan pada fungsi loopPost()
    return string in list
    """
    a = getCaption()
    b = [i[1:] for i in a.split() if i.startswith("#")]
    c = []
    for i in b:
        c.append("#" + i)
    return c

def getComment(): # return list of ten comment
    """
    fungsi yang mereturn Comment dari suatu post
    fungsi dibuat untuk digunakan pada fungsi loopPost()
    return string in list
    """
    alist = []
    try:
        for i in range(1, 11):
            comment = driver.find_element_by_xpath("""/html/body/div[3]/div[2]/div/article/div[2]/div[1]/ul/ul["""+str(i)+"""]/div/li/div/div[1]/div[2]/span""").text
            comment = comment.replace('\r', ' ').replace('\n', ' ')
            comment = ''.join([i if ord(i) < 128 else ' ' for i in comment])    # Remove non ASCII
            alist.append(comment)
    except:
        try:
            comment = driver.find_element_by_xpath("""/html/body/div[3]/div[2]/div/article/div[2]/div[1]/ul/ul/div/li/div/div[1]/div[2]/span""").text
            comment = comment.replace('\r', ' ').replace('\n', ' ')
            comment = ''.join([i if ord(i) < 128 else ' ' for i in comment])    # Remove non ASCII
            alist.append(comment)
            del alist[-1]
        except:
            print("Comment ERROR in number ", datNum)
    finally:
        return alist

def listFormat():
    """
    fungsi untuk format
    """
    alist = [datNum, getAccount(), getCaption(), getHastag(), getLikes(), getComment()]
    return alist

def csvWriter(alist):
    # fungsi untuk menulis ke file csv
    # menggunakan separasi pipe(|)
    global datNum
    row = alist
    with open('DataLevel1.csv', 'a') as csvFile:
        writer = csv.writer(csvFile, delimiter="|")
        if datNum == 1:
            writer.writerow(["", "ACCOUNT:", "POST:", "TAGS:", "LIKES:", "COMMENTS:"])
        writer.writerow(row)
        csvFile.close()
    datNum += 1

def showCSVinPD(file):
    pd.set_option('display.max_rows', 500)
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.width', 2000)
    reviews = pd.read_csv(file, sep="|", index_col=0)
    print(reviews)

def getListUser(UserLevel1): # input adalah list dari nama-nama user yang mau dijadikan patokan
    hasilList = []
    for i in UserLevel1:
        basic = i
        driver.get("https://www.instagram.com/" + basic)
        try:
            folo_button = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a""")
            folo_button.click()
                    
            time.sleep(set_delay)
            nick = driver.find_elements_by_class_name("FPmhX.notranslate._0imsa")
            blist = []
            for j in nick:
                a = j.text
                blist.append(a)
            hasilList = hasilList + blist
        except:
            print("akun", basic, "PRIVATE")
            pass
        time.sleep(5)
    return hasilList

def updateCheckedList():
    global datNum
    alist = []
    blist = []
    with open("DataLevel1.csv", "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter="|")
        for lines in csv_reader:
            if lines:
                some = lines[1]
                num = lines [0]
                alist.append(some)
                alist = list(dict.fromkeys(alist))
                blist.append(num)

    alist.pop(0)
    datNum = int(blist[-1]) + 1
    return alist
    

# Below here is the main program -------------------------------------------------
login()
time.sleep(set_delay)

try:
    checkedList = checkedList + updateCheckedList()
    current_user = random.choice(checkedList)
except:
    pass

if datNum == 1:
    current_user = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/div[1]/h1""").text
    loopPost(current_user)
    checkedList.append(current_user)

def sambung():
    global checkedList
    global current_user
    try:
        checkList = getListUser([current_user])
        checkList = list(dict.fromkeys(checkList))
        for i in checkList:
            if datNum > maxDat:
                 break
            if i in checkedList:
                print("akun sudah di crawl")
            if i not in checkedList:
                loopPost(i)
                try:
                    aka = driver.find_element_by_xpath("""/html/body/div/div[1]/div/div/h2""").text
                except:
                    pass
    finally:
        checkedList = checkedList + checkList
        checkedList = list(dict.fromkeys(checkedList))
        current_user = random.choice(checkedList)

while datNum <= maxDat:
    try:
        checkedList = list(dict.fromkeys(checkedList))
        sambung()
        time.sleep(180)
    except:
        current_user = random.choice(checkedList)
        time.sleep(240)
        print("something wrong")
