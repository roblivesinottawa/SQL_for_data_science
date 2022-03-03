import psycopg2
from config import config
# import sqlalchemy
# from sqlalchemy import create_engine

class Game:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.params = config()

    def connect(self):
        '''Connect to the PostGreSQL Database'''
        try:
            self.conn = psycopg2.connect(**self.params)
            self.cur = self.conn.cursor()
            print('PostgreSQL database version:')
            self.cur.execute('SELECT version()')
            db_version = self.cur.fetchone()
            print(db_version)
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
                print('Database connection closed.')

    def create_tables(self):
        '''creates tables in the database'''
        queries = (
            '''
                CREATE TABLE IF NOT EXISTS  account (
                userid SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL,
                email VARCHAR(250) UNIQUE NOT NULL,
                createdat TIMESTAMP NOT NULL,
                lastlogin TIMESTAMP);
            ''',
            '''
                CREATE TABLE IF NOT EXISTS job (
                jobid SERIAL PRIMARY KEY,
                jobname VARCHAR(200) UNIQUE NOT NULL);
            ''',
            '''
                CREATE TABLE IF NOT EXISTS accountjob (
                userid INTEGER REFERENCES account(userid),
                jobid INTEGER REFERENCES job(jobid),
                hiredate TIMESTAMP);
            '''
           ) 

        self.conn = None
        try:
            self.conn = psycopg2.connect(**self.params)
            self.cur = self.conn.cursor()
            [self.cur.execute(query) for query in queries]
            self.conn.commit()
            print('tables created successfully.')
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            [self.conn.close() if self.conn is not None else None]

    def create_table(self, newtable, data : dict):
        '''creates new table in the database'''
        self.conn = None
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            query = f"""CREATE TABLE {newtable} ({', '.join([f'{key}' for key in data.keys()])})"""
            self.cur.execute(query)
            self.conn.commit()
            print('new table created successfully.')
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            [self.conn.close() if self.conn is not None else None]

    def insert_data(self, table, data : dict):
        '''inserts data into the database'''
        self.conn = None
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            self.cur.execute(f"""INSERT INTO {table} ({','.join(data.keys())}) 
                                VALUES ({','.join(['%s' for _ in range(len(data))])})""",
                                tuple(data.values()))
            self.conn.commit()
            print('data inserted successfully.')
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            [self.conn.close() if self.conn is not None else None]

    def update_data(self, table, data : dict, where : dict):
        '''updates data in the database'''
        self.conn = None
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            self.cur.execute(f"""UPDATE {table} SET {','.join([f'{key}=%s' for key in data.keys()])} 
                                WHERE {','.join([f'{key}=%s' for key in where.keys()])}""",
                                tuple(data.values()) + tuple(where.values()))
            self.conn.commit()
            print('data updated successfully.')
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            [self.conn.close() if self.conn is not None else None]

    def delete_data(self, table, where : dict):
        '''deletes data from the database'''
        self.conn = None
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            self.cur.execute(f"""DELETE FROM {table} 
                                WHERE {','.join([f'{key}=%s' 
                                for key in where.keys()])}""",
                                tuple(where.values()))
            self.conn.commit()
            print('data deleted successfully.')
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            [self.conn.close() if self.conn is not None else None]

    def alter_table_add(self, table, data : dict):
        '''alters table by adding data to the database'''
        self.conn = None
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            self.cur.execute(f"""ALTER TABLE {table} 
                                ADD COLUMN {','.join([f'{key}' for key in data.keys()])}""",
                                tuple(data.values()))
            self.conn.commit()
            print('table altered successfully.')
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            [self.conn.close() if self.conn is not None else None]

    def alter_table_drop(self, table, data : dict):
        '''alters table in the database by dropping data'''
        self.conn = None
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            self.cur.execute(f"""ALTER TABLE {table} 
                                DROP COLUMN {','.join([f'{key}' for key in data.keys()])}""",
                                tuple(data.values()))
            self.conn.commit()
            print('table altered successfully.')
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            [self.conn.close() if self.conn is not None else None]

    def alter_table_rename(self, table, data : dict):
        '''alters table in the database by renaming table'''
        self.conn = None
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            self.cur.execute(f"""ALTER TABLE {table} RENAME TO {data['newname']}""")
            self.conn.commit()
            print('table altered successfully.')
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            [self.conn.close() if self.conn is not None else None]

    def drop_table(self, table):
        '''drops table from the database'''
        self.conn = None
        try:
            params = config()
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor()
            query = f"""DROP TABLE {table}"""
            self.cur.execute(query)
            self.conn.commit()
            print('table dropped successfully.')
            self.cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            [self.conn.close() if self.conn is not None else None]
            

db = Game()
db.connect()

# CREATE 
# db.create_tables()

# INSERT 
# db.insert_data('account', {
#                             'username': 'john', 
#                             'password': 'johnpass123', 
#                             'email': 'john@icloud.com',
#                             'createdat': '2020-01-01',
#                             'lastlogin': '2020-01-01'
#                             })
# db.insert_data('job', {'jobname': 'developer'})
# db.insert_data('job', {'jobname': 'senior web developer'})
# db.insert_data('accountjob', {'userid': 1, 'jobid': 1, 'hiredate': '2020-01-01'})

# UPDATE
# db.update_data('account', {'createdat': 'NOW()'}, {'userid': 1})
# db.update_data('account', {'lastlogin': 'NOW()'}, {'userid': 1})

# DELETE
# db.delete_data('job', {'jobid': 2})

# ALTER
# db.alter_table_rename('information', {'newname': 'information_new'})

# DROP
db.drop_table('information_new')
        