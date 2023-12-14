from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector
import json

app = FastAPI()

# database connnection
conn = mysql.connector.connect(host='localhost', user='root', password='', database='space.db.dev')
cursor = conn.cursor()
class Facts(BaseModel):
	fact_name: str
	fact: str
	author: str

@app.get('/space/hello')
def hello():
	return {
		'Message': 'Hello world'
	}

@app.post('/space/facts/create') # for creating the facts and adding it to the database
def create_facts(facts: Facts):
	if facts.fact_name == " " or facts.fact == " " or facts.author == " ":
		return {
			'Message': 'None of them cannot be empty'
		}
	else:
		sql = 'INSERT INTO `space-facts` (fact_name, fact, author_name) VALUES (%s, %s, %s)'
		values = (facts.fact_name, facts.fact, facts.author)
		cursor.execute(sql, values)
		conn.commit() # for commiting the changes into the database
		return {
			'Successfully created Your facts'
		}


@app.get('/space/fact/viewall') # This endpoint will view all of the facts in the database and writes it into a file
def view_all_facts():
	sql = "SELECT * FROM `space-facts`";
	cursor.execute(sql)
	request = cursor.fetchall()
	filename = 'facts.json'
	with open(filename, 'a') as f:
		json.dump(request, f, indent=5)
		f.close()
	return {
		'Message': f'successfull filename: {filename}'
	}

@app.get('/space/fact/get/count') # get the total number of facts in the database
def get_count():
	sql = "SELECT count(*) From `space-facts`"
	cursor.execute(sql)
	request = cursor.fetchone()
	return {
		'Message': f'You have {request} facts in the database.'
	}

@app.get('/space/fact/view/id/{item_id}') # get the facts based on their ids / number
def get_by_id(item_id: int): # pass the query string with its name and datatype
	try:
		sql = "SELECT fact FROM `space-facts` WHERE id = %s"
		values = (item_id, ) # needs to pass as a tuple or will get an error use , instead of (())
		cursor.execute(sql, values)
		req = cursor.fetchone()
	except HTTPException as e:
		print(f'Something went wrong {e}')

	return req