# %%
import pandas as pd
from email import message_from_string

from neomodel import config, db

import re
import json

from models.employee import Employee, EmailMessage

# %%
def sanitize_email_address(address: str) -> str:
    match = re.search(r'[\w\.-]+@[\w\.-]+', address)
    if match:
        return match.group(0)
    # endif
    return address
# endfunc

def parse_email(email_content: str) -> tuple:
    email = message_from_string(email_content)
    sender = email['from']
    recipient = email['to']
    subject = email['subject']
    cc = email['cc']

    body = ''

    if email.is_multipart():
        for part in email.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))

            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True) 
                break
            # endif
        # endfor
    # endif
    else:
        body = email.get_payload(decode=True)
    # endelse

    return sender, recipient, subject, cc, body.decode('utf-8')
# endfunc

# %%
def filter_recipient_email(rec: str) -> list | str:
    if rec is None:
        return 'None'
    # endif

    recips = rec.split(', ')
    filtered_recips = [sanitize_email_address(r) for r in recips if '@enron.com' in r]

    return filtered_recips if len(filtered_recips) > 0 else 'None'
# endfunc

# %%
def read_config():
    data = None

    with open('./config.json', 'r') as file:
        data = json.load(file)
    #endwith

    return data
# endfunc

def connect_to_n4j():
    db.set_connection(f'{config.DATABASE_URL}/{config.DATABASE_NAME}')
# endfunc
    
# %%
if __name__ == '__main__':
    csv_path = ''
    print('Initializing...')
    app_config = read_config()

    if app_config['db_connection'] is not None:
        config.DATABASE_URL = app_config['db_connection']
    # endif
    else:
        print('Please specify a valid neo4j connection url in the application configuration.')
        exit(1)
    # endelse
    
    if app_config['db_name'] is not None:
        config.DATABASE_NAME = app_config['db_name']
    # endif
    else:
        print('Please specify a valid neo4j database name in the application configuration.')
        exit(1)
    # endelse
    if app_config['data_root_dir'] is not None:
        csv_path = app_config['data_root_dir']
    # endif
    else:
        print('Please specify a valid enron dataset path in the application configuration.')
        exit(1)
    # endelse

    print('Reading Data. This may take a couple of minutes...')
    data = pd.read_csv(csv_path, usecols=['message'])
    data['id'] = data.index
    data[['sender', 'recipient', 'subject', 'cc', 'body']] = data['message'].apply(
        lambda email: pd.Series(parse_email(email))
    )

    print('Processing Emails. This may take a couple of minutes...')
    data.drop(columns=['message'], inplace=True)

    data['sender'] = data['sender'].apply(sanitize_email_address)
    data['recipient'] = data['recipient'].apply(filter_recipient_email)
    data['cc'] = data['cc'].apply(filter_recipient_email)
    data = data[data['recipient'] != 'None']

    data = data[data['sender'].str.contains('@enron.com')]

    try:
        print('Connecting to Graph Database...')
        connect_to_n4j()

        employees = set()

        for sender in data['sender'].to_list():
            employees.add(sender)
        # endfor
            
        for recipients in data['recipient'].to_list():
            for r in recipients:
                employees.add(r)
            # endfor
        # endfor
                
        for cced in data['cc'].to_list():
            if cced != 'None':
                for cc in cced:
                    employees.add(cc)
                # endfor
            # endfor
        # endfor
        
        print('Adding employees:')
        for employee in employees:
            ename = employee.split('@')[0]
            emp = Employee.nodes.get_or_none(emp_name=ename)
            if emp is None:
                print(f'Adding Employee {ename} to database.')
                emp = Employee(emp_name=ename, address=employee).save()
            # endif
            else:
                print(f'Employee {ename} already exists in the database (id: {emp.uid}).')
            # endelse
        #endfor
                
        print('Adding Emails:')
        for row in data.to_numpy().tolist():
            mail = EmailMessage.nodes.get_or_none(mid=row[0])
            if mail is None:
                print(f'Adding email {row[3]} to database.')     
                if row[4] !='None':
                    mail = EmailMessage(
                        mid=row[0],
                        sender=row[1],
                        recipients=row[2],
                        subject=row[3],
                        cc=row[4],
                        body=row[5]
                    ).save()
                # endif
                else:
                    mail = EmailMessage(
                        mid=row[0],
                        sender=row[1],
                        recipients=row[2],
                        subject=row[3],
                        body=row[5]
                    ).save()
                # endelse
            else:
                print(f'Email with subject { row[3] } already exists in the database (mid: {mail.mid}).')
            # endelse
                
            sender_emp = Employee.nodes.get_or_none(address=row[1])
            if sender_emp is not None:
                if not sender_emp.sent_from.is_connected(mail):
                    print(f'SENT_FROM Connecting sender { sender_emp.uid } → mail { mail.mid }.')
                    _ = sender_emp.sent_from.connect(mail)
                # endif
                else:
                    print(f'SENT_FROM sender { sender_emp.uid } → mail { mail.mid } already connected.')
                # endelse
            # endif
                    
            for recipient in row[2]:
                receiver_emp = Employee.nodes.get_or_none(address=recipient)
                if receiver_emp is not None:
                    if not mail.sent_to.is_connected(receiver_emp):
                        print(f'SENT_TO Connecting mail { mail.mid } → {receiver_emp.uid}.')
                        _ = mail.sent_to.connect(receiver_emp)
                    # endif
                    else:
                        print(f'SENT_TO mail { mail.mid } → recipient{receiver_emp.uid} already connected.')
                    # endelse
                # endif
            # endfor
                        
            if row[4] != 'None':
                for ccipient in row[4]:
                    cced_emp = Employee.nodes.get_or_none(address=ccipient)
                    if cced_emp is not None:
                        if not mail.sent_cc.is_connected(cced_emp):
                            print(f'SENT_CC Connecting mail { mail.mid } → {cced_emp.uid}.')
                            _ = mail.sent_cc.connect(cced_emp)
                        # endif
                        else:
                            print(f'SENT_CC mail { mail.mid } → cced employee {cced_emp.uid} already connected.')
                        # endelse
                    # endif
                # endfor
            # endif
    # endtry
    except Exception as e:
        print(f'Unexpected Error: {e}.')
        exit(1)
    # endcatch
# endmain

# endfunc