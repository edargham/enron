from neomodel import db
from models.employee import Employee
from utils import *

def run_query(query: str, db):
  '''
  Base query that accepts any query strings from subsquent functions and returns the result of the query.
  '''
  db = connect_to_n4j(db)
  results, meta = db.cypher_query(query)
  return results, meta

def get_pai_email_activ(topic: str):
  '''
  Returns Lou Pai's email activity with Enron.
  '''
  if topic is None or topic == '':
    return 'Topic cannot be empty.'

  query = f'''
    MATCH (email: EmailMessage)-[:SENT_TO]->(lou: Employee)
    WHERE lou.emp_name = 'lou.pai' AND email.body CONTAINS '{topic}'
    RETURN email, lou
  '''

  results, _ = run_query(query, db)

  print('Lou Pai\'s emails received from Enron on', topic, ':')
  for result in results:
    employee_node = Employee.inflate(result[0])
    sent_count = result[1]
    print(employee_node.name, sent_count)
    for email in employee_node.sent_from:
      print(email.body)
