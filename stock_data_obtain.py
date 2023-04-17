import requests
import json
import time
import ast
import os

# 基于https://gushitong.baidu.com/


def main_func(stock_num):
    time.sleep(1)
    paramer = 0
    li_result = []
    url_1 = (
        "https://finance.pae.baidu.com/selfselect/getstockquotation?code="
        + str(stock_num)
        + "&all=1&ktype=1&isIndex=false&isBk=false&isBlock=false&isFutures=false&stockType=ab&group=quotation_kline_ab&finClientType=pc"
    )
    repsponse = requests.get(url_1)
    check_code = repsponse.status_code  # 200为正确值

    repsponse = repsponse.json()  # 加载为json结构
    repsponse_result = repsponse["Result"]  # request的相关结果

    if len(repsponse_result) < 1: #处理退市的股票
        return li_result
    else:
        for i in range(len(repsponse_result)):
            dict_reult = {"date": "-1", "price": "-1", "volume": "-1", "average_250": "-1"}
            dict_reult["date"] = repsponse_result[len(repsponse_result)-1 - i]["date"]
            dict_reult["price"] = repsponse_result[len(repsponse_result)-1 - i]["kline"]["close"]
            dict_reult["volume"] = repsponse_result[len(repsponse_result)-1 - i]["kline"]["volume"]
            li_result.append(dict_reult)
        paramer = repsponse_result[0]["time"]  # 用于构建下个url的参数

    # 第一次请求url

    while True:
        time.sleep(0.15)
        paramer = int(paramer) - 86400
        url = (
            "https://finance.pae.baidu.com/selfselect/getstockquotation?code="
            + str(stock_num)
            + "&all=0&count=150&ktype=1&isIndex=false&isBk=false&isBlock=false&isFutures=false&stockType=ab&end_time="
            + str(paramer)
            + "&group=quotation_kline_ab&finClientType=pc"
        )
        repsponse = requests.get(url)
        check_code = repsponse.status_code  # 200为正确值
        if check_code != 200:
            print("代码出错！")
            break
        else:
            repsponse = repsponse.json()
            repsponse_result = repsponse["Result"]  # request的相关结果
            if len(repsponse_result) != 150:
                break
            else:
                for i in range(len(repsponse_result)):
                    dict_reult = {
                        "date": "-1",
                        "price": "-1",
                        "volume": "-1",
                        "average_250": "-1",
                    }
                    dict_reult["date"] = repsponse_result[len(repsponse_result) - 1 - i]["date"]
                    dict_reult["price"] = repsponse_result[len(repsponse_result) - 1 - i][
                        "kline"
                    ]["close"]
                    dict_reult["volume"] = repsponse_result[len(repsponse_result) - 1 - i][
                        "kline"
                    ]["volume"]
                    li_result.append(dict_reult)
                    paramer = repsponse_result[0]["time"]  # 用于构建下个url的参数
    return li_result

T1 = time.time()

num_li=[]
name_li=[]
file_open = open("./股票代码.txt", "r", encoding="utf-8", errors="ignore")
lines = file_open.readlines()
for line in lines:
    num =line[0:6]
    name = line[7:len(line)]
    num_li.append(num)
    name_li.append(name)
file_open.close()


# if os.path.exists("./日志.txt"):
#         os.remove("./日志.txt")
print(len(num_li))

for i in range(2123,len(num_li)):
    
    stock_num = num_li[i] 
    name = name_li[num_li.index(stock_num)]
    name = name.replace("\n", "")
    print("正在获取"+name+"的数据>>>>>>>>>>")
    li_result = main_func(stock_num)

    if  len(li_result) == 0:#退市股票
        T2 = time.time()
        print("第##"+str(i)+"##个企业"+name+"已经退市！花费时间："+str(round((T2-T1),2)))
        with open("./日志.txt", "a", encoding="utf-8", errors="ignore") as txt2:
            txt2.write("第##"+str(i)+"##个企业"+name+"已经退市!花费时间："+str(round((T2-T1),2))+"\n")
            time.sleep(0.5)
            # txt2.close()
    else:
        file_name = "./Data_storage/"+name+".txt"
        file_name = file_name.replace("\n",'')
        if os.path.exists(file_name):
            os.remove(file_name)
        file_name = file_name.replace("*",'')
        with open(file_name, "w", encoding="utf-8") as txt1:
            for k in range(len(li_result)):
                txt1.write(str(li_result[k]) + "\n")
        txt1.close()
        T2 = time.time()
        print("第##"+str(i)+"##个企业"+str(name)+"数据获取完成！花费时间："+str(round((T2-T1),2)))
        with open("./日志.txt", "a", encoding="utf-8", errors="ignore") as txt2:
            txt2.write("第##"+str(i)+"##个企业"+name+"数据获取完成!花费时间："+str(round((T2-T1),2))+"\n")
            time.sleep(0.5)
            if i % 8 == 0:
                txt2.close()
        if i % 50 == 0:
            time.sleep(10)
            print("长时间休息！")


# ok——————————————————————————————————————————





