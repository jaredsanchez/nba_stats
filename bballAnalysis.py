import psycopg2
# import pprint


def main():
	#Define our connection string
	conn_string = "host='localhost' dbname='jaredsanchez' user='jaredsanchez' password='Nala2121na'"

	# get a connection, if a connect cannot be made an exception will be raised here
	try:
		conn = psycopg2.connect(conn_string)
	except:
		print "I am unable to connect to the database."

	#make cursor to interact with
	cursor = conn.cursor()

	# cursor.execute("INSERT INTO testTable (id, name) VALUES (1, 'Jared Sanchez')")
	cursor.execute("SELECT * FROM testTable")
	records = cursor.fetchall()
	# pprint.pprint(records)
	print records[0][0]

	conn.commit()
	conn.close()
	# return cursor



#run script
main()


