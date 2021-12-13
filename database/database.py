""" The module allow database manipulations.

:Author: Oleksii Dovhaniuk
:E-mail: dovhaniuk.oleksii@chnu.edu.ua
:Update: 02.01.2021

"""
import sys
sys.path.append('D:/Workspace/Python/projects/QubitLab')

import sqlite3
import pandas as pd

DEFAULT_CSV = 'res/csv/default.csv'

def db_cursor(database):
    """ Function returns cursor of databse connection. 

    :arg: database (str): file name of the fatabase with extantion.

    :return: cursor of the database connection.

    """
    connection = sqlite3.connect(f'database/sqlite/{database}')
    return connection, connection.cursor()

def create_default_gate_table(csv_path = DEFAULT_CSV):
    """ Creates the default gate table in the component database.

    :arg: csv_path (str): By default '<project_folder>/res/csv/default.csv'.

    """
    conn, cur = db_cursor('component.db')
    cur.execute('''
        CREATE TABLE gate(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            designation VARCHAR(255) NOT NULL,
            delay REAL NOT NULL,
            quantum_cost INT NOT NULL,
            basis INT NOT NULL CHECK (basis >= 2) DEFAULT 2);''')

    # Importing csv file.
    df = pd.read_csv(csv_path, keep_default_na=False)   

    # Inserting dataframe to the table.
    for row in df.itertuples():
        cur.execute(f'''
            INSERT INTO gate (id, designation, delay, quantum_cost, basis) 
            VALUES (?, ?, ?, ?, ?);''',
            row[1:])
    conn.commit()
        
def restore_default_component(csv_path = DEFAULT_CSV):
    """ Restors default tables in the component database.

    :arg: csv_path (str): By default '<project_folder>/res/csv/default.csv'.

    """
    conn, cur = db_cursor('component.db')
    cur.execute('DROP TABLE gate;')
    conn.commit()
    create_default_gate_table(csv_path)

    
    
