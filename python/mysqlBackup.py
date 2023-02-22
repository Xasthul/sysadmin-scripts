
# This script provides functionality to delete rows from MySQL database
#   by ID or by entering the whole QUARRY.
# Before the delition, the backup of the database will be made automatically.

import mysql.connector
import os
import time

def dbBackup(mydb):
    backup_dir = "/path/to/backup/directory"
    backup_file = f"{backup_dir}/{time.strftime('%Y%m%d-%H%M%S')}_backup.sql"
    os.system(f"mysqldump -u {mydb.user} -p{mydb._password} {mydb.database} > {backup_file}")
    print(f"Database backed up to {backup_file}")

host = input("MySQL host: ")
user = input("MySQL username: ")
password = input("MySQL password: ")
database = input("MySQL database name: ")
table = input("Table name: ")
mydb = mysql.connector.connect(
  host=host,
  user=user,
  password=password,
  database=database
)

mycursor = mydb.cursor()

choice = input("Delete by ID (1) or write your own QUARRY (2): ")

if(choice == '1'):
    id_to_delete = input("Enter the ID of the row to delete: ")

    sql = f"DELETE FROM {table} WHERE id = {id_to_delete}"

    dbBackup(mydb)
    mycursor.execute(sql)
    mydb.commit()

    print(mycursor.rowcount, "row(s) deleted")

elif(choice == '2'):
    sql = input("Enter the QUARRY to delete: ")

    dbBackup(mydb)
    mycursor.execute(sql)
    mydb.commit()

    print(mycursor.rowcount, "row(s) deleted")
else:
    print("Wrong choce.")
