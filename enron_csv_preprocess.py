# %%
import pandas as pd
from email import message_from_string
from email.parser import Parser

# %%
data = pd.read_csv('E:\\Data Archive\\Datasets\\Enron Emails\\csv\\emails.csv', usecols=['message'])
data

# %%
def parse_email(email_content):
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
data[['sender', 'recipient', 'subject', 'cc', 'body']] = data['message'].apply(
    lambda email: pd.Series(parse_email(email))
)

data.drop(columns=['message'], inplace=True)
data

# %%
data = data[(data['sender'].str.contains('@enron.com')) & (data['recipient'].str.contains('@enron.com')) & (data['cc'].isnull()) | (data['cc'].str.contains('@enron.com'))]
data

# %%



