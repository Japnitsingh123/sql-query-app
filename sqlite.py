import sqlite3

##connect to sqlite
connection=sqlite3.connect("student.db")

##create a cursor to insert recored,create table
cursor=connection.cursor()

##TABLE 
table_info="""
CREATE TABLE STUDENT(
NAME VARCHAR(25),
CLASS VARCHAR(25),
SECTION VARCHAR(25)
);
"""
##CREATE TABLE
cursor.execute(table_info)

##insert some record

cursor.execute("""Insert into STUDENT values('Ram','Physics','A') """)
cursor.execute("""Insert into STUDENT values('Sudhir','Chem','B') """)
cursor.execute("""Insert into STUDENT values('Manish','Maths','C') """)
cursor.execute("""Insert into STUDENT values('Angad','English','D') """)

##display all the record
print("the records are")
data=cursor.execute("""select * from STUDENT""")
for row in data:
    print(row)

connection.commit()
connection.close()


