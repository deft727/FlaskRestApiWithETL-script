import requests
import json
import sqlite3


with sqlite3.connect("mydatabase.db") as conn:
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT)'''
    )


count=0
while count!=100:
    
    url=  requests.get('https://randomuser.me/api/')
    if url.status_code==503:
        url=  requests.get('https://randomuser.me/api/')
        if url.status_code!=503:
            data=url.json()
        else:
            url=  requests.get('https://randomuser.me/api/')
    else:
        data=url.json()


    for i in data['results']:
        if i['gender']=='male':
            count+=1
            print(i['name']['first'],count)
            first_name=i['name']['first']
            last_name=i['name']['last']
            with conn:
                cur = conn.cursor() 
                cur.execute("INSERT INTO users VALUES (NULL,?,?)",(first_name, last_name))
