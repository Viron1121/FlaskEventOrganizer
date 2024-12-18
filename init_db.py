import sqlite3

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO reservation (fullname, address,contact,emailaddress,age,sex,category, date, time,package ,status) VALUES (?, ?, ?, ?, ?,?,?,?,?,?,?)",
            ('John Lloyd', 'Pila', '09657029069', 'johnlloydlacadin042301@gmail.com', '18' , 'Male' , 'birthday','date','time','package','pending')
            )

cur.execute("INSERT INTO users (fullname, username,password) VALUES (?, ?, ?)",
            ('fullname', 'username', 'password')
            )

cur.execute("INSERT INTO packages (packagename, description, price, person, food,img) VALUES (?, ?, ?, ?, ?,?)",
            ('Big Wedding', 'sample description', '20,000', '20-50','Korean Food','wew.jpg')
            )

connection.commit()
connection.close()
