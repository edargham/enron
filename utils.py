import json

# %%
def read_config():
  data = None

  with open('./config.json', 'r') as file:
    data = json.load(file)
  #endwith

  return data
# endfunc

def connect_to_n4j(db):
    config = read_config()
    db.set_connection(f'{config["db_connection"]}/{config["db_name"]}')
    return db
# endfunc