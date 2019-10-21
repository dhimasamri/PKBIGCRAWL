import pandas as pd
import csv

data_list = []
proced_data_ke = 1
data_max = 0
first_time = 1

def getDataFromLevel1():
    global data_list
    with open("DataLevel1.csv", 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter='|')
        for row in reader:
            if row:
                data_list.append(row)
    csvFile.close()

def text_to_list(text):
    text = text.lower()
    text = text.split()
    list_text = []
    if len(text) < 2:
        return
    for i in range(len(text)):
        if text[i][0] == '#' or text[i][0] == '@':
            break
        kataSementara = ''
        for z in text[i]:
            if ord(z) == 126:
                kataSementara = kataSementara+' '
            elif ord(z) > 96 and ord(z) < 123:
                kataSementara = kataSementara + z
        if kataSementara:
            list_text.append(kataSementara)
    return list_text

def pairing(user, list_of_text):
    global first_time
    alist = list_of_text
    a = {}
    if alist == None:
        return
    for i in range(len(alist)-1):
        try:
            a[alist[i]][alist[i+1]] += 1
        except:
            a[alist[i]] = {(alist[i+1]) : 1}

    # menulis ke dataFrame
    dfObj = pd.DataFrame(columns=['User', 'Word1', 'Word2', 'Freq'])
    for j in a:
        for k in a[j]:
            dfObj = dfObj.append({'User' : user, 'Word1' : j, 'Word2' : k, 'Freq' : a[j][k]}, ignore_index = True)
    if first_time:
        dfObj.to_csv('DataLevel2.csv', mode = 'a', header = True, sep = "|", index = False)
        first_time = 0
    else:
        dfObj.to_csv('DataLevel2.csv', mode = 'a', header = False, sep = "|", index = False)

# main program ---------------------------------------
getDataFromLevel1()
data_max = int(data_list[-1][0])
indi = True
while proced_data_ke <= data_max:
    print(proced_data_ke)
    cur_user = data_list[proced_data_ke][1]
    kalimat = data_list[proced_data_ke][2]
    a = text_to_list(kalimat)
    pairing(cur_user, a)
    proced_data_ke += 1
