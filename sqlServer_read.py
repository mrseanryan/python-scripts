# script to read from SQL Server DB
#
# Dependencies:  Python, pyodbc, SQL Server
#
# Python 2.7
# pyodbc 2.1.9 Windows 32-bit
#
# ref:  http://www.simple-talk.com/sql/database-administration/python-for-the-sql-server-dba/

import pyodbc as p
import re #RegEx library

server = '.'  #local server
database = 'Acquirer'

connStr = ( r'DRIVER={SQL Server};SERVER=' +
	server + ';DATABASE=' + database + ';' +
	'Trusted_Connection=yes'    )

conn = p.connect(connStr)
dbCursor = conn.cursor()
sql = ("select name from MC_Merchant order by name")
dbCursor = conn.cursor()
dbCursor.execute(sql)
for row in dbCursor:
	print row.name + ", "

conn.close()

print ("[done]")
