import requests
import json
import time
import ast
import os
import random
import pandas as pd


def update_record(
    stock_num, stock_name, file_name
):  # 数据更新到今天,file_name保存文件路径  "./Data_storage/  "；

    url_1 = (
        "https://finance.pae.baidu.com/selfselect/getstockquotation?code="
        + str(stock_num)
        + "&all=1&ktype=1&isIndex=false&isBk=false&isBlock=false&isFutures=false&stockType=ab&group=quotation_kline_ab&finClientType=pc"
    )
    headers = {
        "cookie": 'BIDUPSID=E200EDA83E074C23FCE2EEA5DC8C8AD8; PSTM=1633410607; __yjs_duid=1_531279aea478297b89ef6b1d8fef08851633411310778; BDUSS=XpOTUtJa2tqTH5WWjJHWDN4Zn5EWkUyfjVIWURja05VfmFReGtrai1VRnVkWlpqRVFBQUFBJCQAAAAAAAAAAAEAAAB7o~44t8rF1rXE0KGw1zEyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG7obmNu6G5jO; BDUSS_BFESS=XpOTUtJa2tqTH5WWjJHWDN4Zn5EWkUyfjVIWURja05VfmFReGtrai1VRnVkWlpqRVFBQUFBJCQAAAAAAAAAAAEAAAB7o~44t8rF1rXE0KGw1zEyAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAG7obmNu6G5jO; BAIDUID=9E290503A0E0C10D0A3D0981831B1B58:SL=0:NR=10:FG=1; MAWEBCUID=web_XkVgDViXDPCMAUDXIjPHslevBiyMyPZuZUzsSoNsCWTbshtwec; MCITY=-289%3A; BA_HECTOR=0g04202h2h2h0401a085ak4b1i0oii81n; BAIDUID_BFESS=9E290503A0E0C10D0A3D0981831B1B58:SL=0:NR=10:FG=1; ZFY=AYJfzlsePrECDSME8y1HzUIWg8q:ADYy1gTMcNpj2VHQ:C; BAIDU_WISE_UID=wapp_1678528936358_746; arialoadData=false; RT="z=1&dm=baidu.com&si=42aec432-33e1-4310-9401-ae3a9f070171&ss=lf3ssk0b&sl=6&tt=53c&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&nu=m15a1vqx&cl=k03&ld=lw7&ul=33v11&hd=33v2m'
    }
    repsponse = requests.get(url_1, headers=headers)
    check_code = 0
    check_code = repsponse.status_code  # 200为正确值

    repsponse = repsponse.json()  # 加载为json结构
    repsponse_result = repsponse["Result"]  # request的相关结果

    li_date_check = []
    history_record = []
    for l in range(len(repsponse_result)):
        li_date_check.append(repsponse_result[l]["date"])

    if len(li_date_check) == 0:
        print("url返回错误")
        return -1

    file_name = str(file_name) + stock_name + ".txt"
    with open(file_name, "r", encoding="utf-8") as txt1:
        lins = txt1.readlines()
        line = ast.literal_eval(lins[0])  # 字符串转为字典格式

        for line_1 in lins:
            history_record.append(line_1)  # txt中已有信息存起来

    latest_date = line["date"]
    if latest_date in li_date_check:
        index_date = li_date_check.index(latest_date)
    else:
        return -1

    li_result = []
    for i in range(index_date + 1, len(repsponse_result)):
        dict_reult = {
            "date": "-1",
            "price": "-1",
            "volume": "-1",
            "average_250": "-1",
        }
        dict_reult["date"] = repsponse_result[i]["date"]
        dict_reult["price"] = repsponse_result[i]["kline"]["close"]
        dict_reult["volume"] = repsponse_result[i]["kline"]["volume"]
        li_result.append(dict_reult)

    with open(file_name, "w", encoding="utf-8") as txt1:
        for i in range(len(li_result)):
            txt1.write(str(li_result[len(li_result) - i - 1]) + "\n")

        for i in range(len(history_record)):
            txt1.write(str(history_record[i]))
    txt1.close()
    return 1


def Create_Operate_Date_set(file_name):  # 构建单个股票可操作的数据集
    Date_list = []
    with open(file_name, encoding="utf-8") as txt1:
        lines = txt1.readlines()
        for line in lines:
            line = ast.literal_eval(line)
            Date_list.append(line)
    return Date_list


def Calculate_Average_of_parmar(
    Date_list, Calculate_parameter, time_interval, Result_parameter
):  # 计算均值d
    Calculate_li = []
    for i in range(time_interval):
        price = float(Date_list[i][Calculate_parameter])
        Calculate_li.append(price)

    average_price = round(sum(Calculate_li) / time_interval, 3)
    Date_list[1][Result_parameter] = average_price
    for l in range(1, len(Date_list) - (time_interval + 50)):
        index = (l - 1) % time_interval
        Calculate_li[index] = float(Date_list[l + time_interval][Calculate_parameter])
        average_price = round(sum(Calculate_li) / time_interval, 3)
        Date_list[l + 1][Result_parameter] = average_price


def Add_key_To_Data_li(Data_li, key):  # 增加键值
    x = key in Data_li[1]
    if x == 1:
        return 0
    else:
        for line in Data_li:
            line[str(key)] = -1


def Delete_key_from_Data_li(Data_li, key):  # 删除加键值
    x = key in Data_li[1]
    if x == 0:
        return 0
    else:
        for line in Data_li:
            line.pop(key)


def Creat_li_of_a_key(Data_li, key):  # 把某一个股票的某一个键转成list用以分析
    result_li = []
    for line in Data_li:
        if key in line:
            result = line[key]
            result_li.append(result)
        else:
            return result_li
    return result_li


def update_All_Dates(list_All_stocks,start_num, a,):  # 根据所有股票的名称更新所有股票的相关数据；a==1时执行
    if a == 1:
        for i in range(start_num, len(list_All_stocks)):
            time.sleep(1)
            name = list_All_stocks[i]
            name_1 = name.replace("*", "")
            name_1 = name.replace("ST", "")
            for j in range(6):  # 尝试获取数据
                a = update_record(Dic_name_and_num[name_1], name, "./Data_storage/")
                if a == 1:
                    with open(
                        "./日志2.txt", "a", encoding="utf-8", errors="ignore"
                    ) as txt3:
                        txt3.write(
                            "第\t" + str(i) + "\t个企业\t" + name + "\t的数据更新————ok！\n"
                        )
                        txt3.close()
                    print("第\t" + str(i) + "\t个企业\t" + name + "\t的数据更新————ok！")
                    break
                else:
                    with open(
                        "./日志2.txt", "a", encoding="utf-8", errors="ignore"
                    ) as txt3:
                        txt3.write("第\t" + str(i) + "\t个企业\t" + name + "\t---erro！\n")
                        txt3.close()
                    # time.sleep(5)
                    time.sleep(random.uniform(2, 3))
        txt3.close()
    else:
        return 0


def Across_mean(Date, Avera_data, times):  # 均值和每日数据“四渡赤水”情况分析
    j = 0
    i = 0
    num = 0
    for i in range(len(Date)):
        if i == num:
            if i >= len(Avera_data):
                return -1
            else:
                if float(Date[i]) - float(Avera_data[i]) >= 0:
                    while float(Date[num]) - float(Avera_data[num]) >= 0:
                        num = num + 1
                        if num == len(Avera_data):
                            return -1
                    j = j + 1
                else:
                    while float(Date[num]) - float(Avera_data[num]) < 0:
                        num = num + 1
                        if num == len(Avera_data):
                            return -1
                    j = j + 1
                if j == times:
                    return num
                    break


T1 = time.time()
num_li = []
name_li = []
file_open = open("./股票代码.txt", "r", encoding="utf-8", errors="ignore")
lines = file_open.readlines()
for line in lines:
    num = line[0:6]
    name = line[7 : len(line) - 1]
    num_li.append(num)
    name = name.replace("*", "")
    name = name.replace("ST", "")
    name_li.append(name)
file_open.close()
Dic_name_and_num = dict(zip(name_li, num_li))  # 名称和代码对应的字典（用于在线更新数据）
path = "./Data_storage"  # 文件目录
datanames = os.listdir(path)
list_All_stocks = []  # TXT中的所有文件名称形成列表（最后在这个里面循环）
for i in datanames:
    i = i.replace(".txt", "")
    list_All_stocks.append(i)

# ___________________________________________________这个函数不要每天都执行!!!
update_All_Dates(list_All_stocks, 0, 0)  # 最后参数等于1时执行，倒数第二个参数为“第x个股票”；共2375个股票
# ——————————————————————————————————————————————————————————————————————

# li_calculated = []

for i in range(0, len(datanames)):
    file_name = path + "/" + str(datanames[i])
    Data_li = Create_Operate_Date_set(file_name)

    # Delete_key_from_Data_li(Data_li, "average_250")  # 删除字段
    # Calculate_Average_of_parmar(Data_li, "price", 250, "Price_Ave_250")

    # with open(file_name, "w", encoding="utf-8") as txt1:#数据保存回txt文件中
    #     for line in Data_li:
    #         txt1.write(str(line) + "\n")
    Data_li.pop(0)
    price_li = Creat_li_of_a_key(Data_li, "price")
    average_250_li = Creat_li_of_a_key(Data_li, "Price_Ave_250")
    Days = Across_mean(price_li, average_250_li, 8)
    li_calculated.append(Days)
    T2 = time.time()
    T_total = round((T2 - T1), 3)
    print(i, Days, list_All_stocks[i], T_total)

df = pd.DataFrame({"Name": list_All_stocks, "Days": li_calculated})
df.to_csv("./结果.txt")

# file_name = "./埃斯顿.txt"
# Data_li = Create_Operate_Date_set(file_name)
# Delete_key_from_Data_li(Data_li, "average_100")  # 删除字段
# Calculate_Average_of_parmar(Data_li, "price", 250, "average_250")  # 根据某一字段计算相应的平均值并进行保存
# with open(file_name, "w", encoding="utf-8") as txt1:  # 数据保存回txt文件中
#     for line in Data_li:
#         txt1.write(str(line) + "\n")


# price_li = Creat_li_of_a_key(Data_li, "price")
# average_250_li = Creat_li_of_a_key(Data_li, "average_250")
# # 用于分析的Data_list
# Data_li_for_analyze = Create_Operate_Date_set(file_name)
# Data_li_for_analyze.pop(0)


# a = Across_mean(price_li, average_250_li, 2)
# print(a)

# print(Data_li[1])
