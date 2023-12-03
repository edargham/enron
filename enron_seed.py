from neomodel import config, db

import os
import json
import numpy

from models.employee import Employee

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

if __name__ == '__main__':
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

    root_dir = ''
    if app_config['data_root_dir'] is not None:
        root_dir = app_config['data_root_dir']
    # endif
    else:
        print('Please specify a valid enron dataset path in the application configuration.')
        exit(1)
    # endelse
    try:
        connect_to_n4j()
        employees = os.listdir(root_dir)

        if (len(employees) != 150):
            print('Dataset is not a valid enron users dataset.')
            exit(1)
        # endif

        for employee in employees:
            emp = Employee.nodes.get_or_none(emp_name=employee)
            if emp is None:
                print(f'Adding Employee {employee} to database.')
                emp = Employee(emp_name=employee).save()
            # endif
            else:
                print(f'Employee {employee} already exists in the database (id: {emp.uid}).')
            # endelse
        #endfor
    # endtry
    except Exception as e:
        print(f'Unexpected Error: {e}.')
        exit(1)
    # endcatch
# endmain