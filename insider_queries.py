from neomodel import db
from models.employee import EmailMessage, Employee
from utils import *


def run_query(query: str, db):
  '''
  Base query that accepts any query strings from subsquent functions and returns the result of the query.
  '''
  db = connect_to_n4j(db)
  results, meta = db.cypher_query(query)
  return results, meta
# endfunc

def get_ljm_lay_affair():
  '''
  Prints the LJM email Activity by Lay.
  '''
  
  query = '''
    MATCH (incom_email: EmailMessage)-[:SENT_TO]->(lay: Employee {emp_name: 'kenneth.lay'})
    WHERE  incom_email.body CONTAINS 'LJM'
    RETURN incom_email, lay
  '''

  results, _ = run_query(query, db)

  print('Kenneth\'s involvement with the LJM affair:')
  for result in results:
    email_node = EmailMessage.inflate(result[0])
    print('Message Id:', email_node.mid)
    print(email_node.subject)

    print('Sent to:')
    for employee in email_node.sent_to:
      print(employee.emp_name)
    # endfor
      
    print('body:')
    print(email_node.body)
    print()
  # endfor
# endfunc
    
def get_ews_ljm_conenction():
  '''
  Prints the relationship between the EWS litigation and the LJM affair.
  '''
  query = '''
    MATCH (emp_sender: Employee)-[:SENT_FROM]->(email: EmailMessage)-[:SENT_TO]->(emp_recv: Employee)
    WHERE  email.body CONTAINS 'EWS' AND email.body CONTAINS 'LJM'
    RETURN emp_sender, email, emp_recv
  '''

  results, _ = run_query(query, db)

  for result in results:
    print('Sender:', Employee.inflate(result[0]).emp_name)
    email_sent = EmailMessage.inflate(result[1])
    print('Subject:', email_sent.subject)
    print('Recipients:')

    for recv in email_sent.sent_to:
      print(recv.emp_name)
    # endfor
      
    print()
  # endfor
# endfunc
    
def get_ews_investigation_scope():
  '''
  Prints the entire scope of emails about the EWS investigation.
  '''

  query = '''
    MATCH (emp_sender: Employee)-[:SENT_FROM]->(email: EmailMessage)-[:SENT_TO]->(emp_recv: Employee)
    WHERE  email.subject CONTAINS 'EWS Litigation'
    RETURN emp_sender, email, emp_recv
  '''

  results, _ = run_query(query, db)

  for result in results:
    print('Sender:', Employee.inflate(result[0]).emp_name)
    email_sent = EmailMessage.inflate(result[1])
    print('Subject:', email_sent.subject)
    print('Recipients:')

    for recv in email_sent.sent_to:
      print(recv.emp_name)
    # endfor
      
    print()
  # endfor
# endfunc