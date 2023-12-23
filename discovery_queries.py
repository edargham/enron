from neomodel import db
from models.employee import Employee, EmailMessage
from utils import *


def run_query(query: str, db):
  db = connect_to_n4j(db)
  results, meta = db.cypher_query(query)
  return results, meta

def get_most_active_employees(lim: int=10):
  query = f'''
    MATCH (sender:Employee)-[sent_from:SENT_FROM]->(email:EmailMessage)
    WITH sender, COUNT(sent_from) AS sent
    RETURN sender, sent
    ORDER BY sent DESC
    LIMIT {lim}
  '''

  results, _ = run_query(query, db)

  for result in results:
    employee_node = Employee.inflate(result[0])
    sent_count = result[1]
    print(employee_node.name, sent_count)

def num_email_sent_from_sender (lim: int = 50):
  query = f'''MATCH (sender:Employee)-[sent_from:SENT_FROM]->(email:EmailMessage)
WITH sender, COUNT(sent_from) as sent_count
MATCH (sender:Employee)
OPTIONAL MATCH (sender)-[sent_from:SENT_FROM]->(email:EmailMessage)
RETURN sender, COLLECT(email)[..5], sent_count
ORDER BY sent_count DESC
LIMIT 50'''
  
  results, _  = run_query(query,db)

  for result in results:
    employee_node = Employee.inflate(result[0])
    emails = result[1]
    sent_count = result[2]
    print(employee_node.name, sent_count, emails)    

def num_email_sent_from_sender_without_cc (lim: int = 150):
  query = f'''
MATCH (sender:Employee)-[sent_from:SENT_FROM]->(email:EmailMessage)
WITH sender, COUNT(sent_from) as sent_count
MATCH (sender:Employee)
OPTIONAL MATCH (sender)-[sent_from:SENT_FROM]->(email:EmailMessage)
WHERE email.cc IS NULL
RETURN sender, COLLECT(email)[..5], sent_count
ORDER BY sent_count DESC
LIMIT 100'''
  
  results, _ = run_query(query, db)

  for result in results:
    employee_node = Employee.inflate(result[0])
    emails = result[1]
    sent_count = result[2]
    print(employee_node.name, sent_count, emails)    
  
  
