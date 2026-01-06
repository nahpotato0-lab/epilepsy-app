import mysql.connector
import sys

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="sql123",
  database="darsh"
)
cursor = mydb.cursor(buffered=True)
query = "TRUNCATE TABLE epilepsy;"
video_hash = 372040820107144080
cursor.execute(query)
row = cursor.fetchall()
print(row)
cursor.close()
mydb.close()
# print(row)
# if row:
#     rows = [x for x in row]
#     # write_to_file(lzma.decompress(rows[0]))
#     video_data = bytes((rows[0]))
#     print(video_data.__sizeof__())
# query = """CREATE TABLE epilepsy (
#   hash BIGINT UNSIGNED PRIMARY KEY, 
#   time_uploaded DATETIME NOT NULL, 
#   title TEXT, 
#   movie LONGBLOB
#   )
# """

# mycursor.execute(query)
# '''
# TYPING- 
# UNSIGNED BIGINT hash // unique ID, hash of title and time uploaded
# DATETIME time_uploaded 
# TEXT title
# LONGBLOB movie // movie being accessed
# '''

