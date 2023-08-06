import redshift_connector
import cx_Oracle
from google.cloud import bigquery
import pyodbc
from boto.s3.connection import S3Connection
import snowflake.connector

#Will contain the methods for connecting to the databases.
def oracle( host,port, sid,username, pwd,service_name):
	conn=""
	if service_name!="":
		dsn = cx_Oracle.makedsn(host=host, port=port, sid=sid)
		conn = cx_Oracle.connect(user=username, password=pwd, dsn=dsn)

	if sid!="":
		dsn = cx_Oracle.makedsn(host=host, port=port, service_name=service_name)
		conn = cx_Oracle.connect(user=username, password=pwd, dsn=dsn)
	return conn

def sql_server(driver,server,database,uid,password):
	conn_string="DRIVER={"+str(driver)+"};"+"SERVER="+str(server)+";"+"DATABASE="+str(database)+";"+"UID="+uid+";"+"PWD="+str(password)
	conn = pyodbc.connect(conn_string)
	#creating the cursor
	cursor = conn.cursor()
	return conn

def snow(user,password, account,warehouse,database,schema):
	conn = snowflake.connector.connect(
                user=user,
                password=password,
                account=account,
                warehouse=warehouse,
                database=database,
                schema=schema
                )
	return conn

def aws_redshift(host,database_name,user, password):
	conn = redshift_connector.connect(
    host=host,
    database=database_name,
    user=user,
    password=password
    )
    #creating the cursor
	cursor: redshift_connector.Cursor = conn.cursor()
	return conn
   
def google_bigquery(username, pwd, hyperlink, database_name):
	client = bigquery.Client()
	return client

def amazon_s3(aws_access_key,aws_secret_key):
	conn = S3Connection(aws_access_key,aws_secret_key)
	return conn





