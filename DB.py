import mysql.connector
from mysql.connector import errorcode
from config import user, password, host, database

def _table_exist(id: str) -> bool: # Checks if table exists
	cnx = mysql.connector.connect(user=user, 
									  password=password,
		                              host=host,
		                              database='information_schema')
	cursor = cnx.cursor()

	cursor.execute("select count(table_name) from tables where table_name = '{}';".format(id))
	num = 0
	for i in cursor:
		num += i[0]
	cnx.close()
	return num > 0



def _create_user_table(id:str) -> None: # Creates table with given name

	try:
		cnx = mysql.connector.connect(user=user, 
									  password=password,
		                              host=host,
		                              database=database,
		                              )
		cursor = cnx.cursor()
	except mysql.connector.Error as err:
	  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
	    print("Something is wrong with your user name or password")
	  elif err.errno == errorcode.ER_BAD_DB_ERROR:
	    print("Database does not exist")
	  else:
	    print(err)

	table_description = (
		"CREATE TABLE `{}` ("
	    "  `ID` int(11) NOT NULL AUTO_INCREMENT,"
	    "  `item` varchar(32) NOT NULL,"
	    "  PRIMARY KEY (`ID`))")
	cursor.execute(table_description.format(id))
	cnx.close()

def drop(id: str) -> None: # Deletes given table

	tab = 'user'+ str(id)

	if not _table_exist(tab): _create_user_table(tab)

	try:
		cnx = mysql.connector.connect(user=user, 
									  password=password,
		                              host=host,
		                              database=database,
		                              )
		cursor = cnx.cursor()
	except mysql.connector.Error as err:
	  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
	    print("Something is wrong with your user name or password")
	  elif err.errno == errorcode.ER_BAD_DB_ERROR:
	    print("Database does not exist")
	  else:
	    print(err)

	drop_query = "DROP TABLE {table}"
	cursor.execute(drop_query.format(table = tab))
	cnx.commit()
	cnx.close()

def delete_from_list(id: int, item: str) -> None: # Deletes item from users shopping list

	tab = 'user'+ str(id)

	if not _table_exist(tab): _create_user_table(tab)

	try:
		cnx = mysql.connector.connect(user=user, 
									  password=password,
		                              host=host,
		                              database=database,
		                              )
		cursor = cnx.cursor()
	except mysql.connector.Error as err:
	  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
	    print("Something is wrong with your user name or password")
	  elif err.errno == errorcode.ER_BAD_DB_ERROR:
	    print("Database does not exist")
	  else:
	    print(err)

	delete_query = "DELETE FROM {table} where item = '{line}';"

	cursor.execute(delete_query.format(table = tab, line = item))
	cnx.commit()
	cnx.close()

def insert_into_list(id: id, item: str) -> None: # Adds item to users shopping list

	tab = 'user'+ str(id)

	if not _table_exist(tab): _create_user_table(tab)

	try:
		cnx = mysql.connector.connect(user=user, 
									  password=password,
		                              host=host,
		                              database=database
		                              )
		cursor = cnx.cursor()
	except mysql.connector.Error as err:
	  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
	    print("Something is wrong with your user name or password")
	  elif err.errno == errorcode.ER_BAD_DB_ERROR:
	    print("Database does not exist")
	  else:
	    print(err)

	insertion_query = "INSERT INTO {table} (item) values ('{line}');"

	cursor.execute(insertion_query.format(table = tab, line = item))
	cnx.commit()
	cnx.close()

def read_list(id: int) -> list: # Returns unsorted shopping list
	tab = 'user'+ str(id)

	if _table_exist(tab):
		try:
			cnx = mysql.connector.connect(user=user, 
									  	  password=password,
		                              	  host=host,
		                              	  database=database
		                              	  )
			cursor = cnx.cursor()
		except mysql.connector.Error as err:
		  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		    print("Something is wrong with your user name or password")
		  elif err.errno == errorcode.ER_BAD_DB_ERROR:
		    print("Database does not exist")
		  else:
		    print(err)

		read_query = "SELECT item FROM {};"

		cursor.execute(read_query.format(tab))
		output = []
		for i in cursor:
			output += i
		cnx.close()
	else:
		output = []
	return output

if __name__ == '__main__':

	inp = input()
	print(read_list(inp))

