import sqlite3
import csv

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database
    '''

    # Get the database running
    def __init__(self, database_arg="./temp3.db"):
        self.data_directory="./data"
        self.conn = sqlite3.connect(database_arg,check_same_thread=False)
        self.cur = self.conn.cursor()
        self.to_read_list=["Games_Feture_Engineering","user"]




    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------


    # Drop table if you want to reconstruct the table, can be usually used on user 
    def drop_table(self,tablename):
        self.cur.execute("DROP TABLE IF EXISTS {}".format(tablename))
        self.conn.commit()






    # Only reconstruct the register part database
    def database_reconstruct_login_part(self):
        self.drop_table("Userpassword")
        self.drop_table("Sessions")
        

        self.cur.execute("""CREATE TABLE Userpassword(
            username TEXT,
            password TEXT
        )""")

        self.conn.commit()


        self.cur.execute("""CREATE TABLE Sessions(
            session_id TEXT,
            username TEXT,
            expiry_time TEXT
        )""")


        self.conn.commit()



    # Make sure you have add user.csv into the db before use this function
    def database_add_default_users_to_Userpassword(self):
        self.cur.execute("SELECT * FROM user")
        rows = self.cur.fetchall()


        
        # Insert the fetched rows into the new table
        count=0
        for row in rows:
            # print(row)
            if count%10000==0:
                print(count)
            self.cur.execute("INSERT INTO Userpassword (username, password) VALUES (?, ?)", (row[0],row[0]))
            count=count+1
        # Commit the changes and close the database connection
        self.conn.commit()

        









    # Only construct the register part database
    def database_construct_login_part(self):


        self.cur.execute("""CREATE TABLE Userpassword(
            username TEXT,
            password TEXT
        )""")

        self.conn.commit()


        self.cur.execute("""CREATE TABLE Sessions(
            session_id TEXT,
            username TEXT,
            expiry_time TEXT
        )""")


        self.conn.commit()






    # Sets up the database
    # Default admin password
    def database_setup(self):



        self.cur.execute("""CREATE TABLE Userpassword(
            username TEXT,
            password TEXT
        )""")

        self.conn.commit()

        self.cur.execute("""CREATE TABLE Sessions(
            session_id TEXT,
            username TEXT,
            expiry_time TEXT
        )""")

        self.conn.commit()





        # Read game data and rating data 
        for i in self.to_read_list:
            self.cur.execute("DROP TABLE IF EXISTS {}".format(i))
            self.conn.commit()




        for i in self.to_read_list:
            print(i)
            with open(self.data_directory+i+".csv", 'r') as f:
                reader = csv.reader(f)
                headers = next(reader)


            # print(headers)
            headers=[col_name.replace('\ufeff', '') for col_name in headers]

            # Because adding : to sql make problem
            headers=[col_name.replace(':', '__') for col_name in headers]
            # print(len(headers))

            s = 'CREATE TABLE {} ({})'.format(i,', '.join([f'{col} text' for col in headers]))
            print(s)
            self.cur.execute(s)
            self.conn.commit()
            print("\n\n")






    def add_all_rows(self,filename,tablename):

        filename=self.data_directory+filename


        self.cur.execute("BEGIN TRANSACTION")

        with open(filename, 'r',encoding="utf-8-sig") as f:
            
            reader = csv.reader(f)
            data = list(reader)
            headers = data[0]
            headers=[col_name.replace('\ufeff', '') for col_name in headers]

            # Because adding : to sql make problem
            headers=[col_name.replace(':', '__') for col_name in headers]


            column_names = ', '.join(headers)
            placeholders = ', '.join(['?'] * len(headers))

        count=0



        for row in data[1:]:

            if count%10000==0:
                print(count)


            self.cur.execute(f"INSERT INTO {tablename} ({column_names}) VALUES ({placeholders})", row)
            self.conn.commit()

            count=count+1



        self.cur.execute('SELECT * FROM {} ORDER BY RANDOM() LIMIT 1'.format(tablename))
        row = self.cur.fetchone()

        print(row)
                    







    def get_all_rating_by_userid(self,userid):

        query = "SELECT * FROM user_ratings where UserId=? "

        self.cur.execute(query,(userid,))

        # If our query returns
        line=self.cur.fetchall()
        # print(line)
        if line:
            return line
        else:
            return False










    def view_attribute(self,table_name):
        
        self.cur.execute(f"PRAGMA table_info({table_name})")

        ## Print the table information


        
        # print("Column attributes for table:", table_name)
        # print("cid | name | type | notnull | dflt_value | pk")

        result=self.cur.fetchall()
        # for row in result:
        #     print(row)
        return result







    # # Add a user to the database
    def add_u(self,username,password):

        query = "INSERT INTO Userpassword (username, password) VALUES (?, ?)"

        # Execute the query with user input as a parameter

        self.cur.execute(query, (username,password,))
        self.conn.commit()


        return True






    # Check whether register
    def check_u_register(self,username):

        query = "SELECT * FROM Userpassword where username=? "

        self.cur.execute(query,(username,))

        # If our query returns
        line=self.cur.fetchone()
        # print(line)
        if line:
            return line
        else:
            return False






    # Check login credentials
    def get_u(self,username,password):

        query = "SELECT * FROM Userpassword where username=? and password=?"

        self.cur.execute(query,(username,password,))

        # If our query returns
        line=self.cur.fetchone()
        # print(line)
        if line:
            return line
        else:
            return False




    def get_game(self,keyword):
        query = "SELECT * FROM Games_Feture_Engineering WHERE Name LIKE ?"
        params = ('%{}%'.format(keyword),)

        self.cur.execute(query, params)

        # If our query returns
        line=self.cur.fetchall()
        # print(line)
        if line:
            return line
        else:
            return False


    def get_specific_game_by_gameid(self,keyword):
        query = "SELECT * FROM Games_Feture_Engineering WHERE BGGId = ?"
        params = ('{}'.format(keyword),)

        self.cur.execute(query, params)

        # If our query returns
        line=self.cur.fetchone()
        # print(line)
        if line:
            return line
        else:
            return False



    def select_top_n_game_by_column(self,column,top_n,):

        query = "SELECT * FROM Games_Feture_Engineering ORDER BY ? DESC LIMIT ?"
  

        self.cur.execute(query, (column,top_n,))

        # If our query returns
        line=self.cur.fetchall()
        # print(line)
        if line:
            return line
        else:
            return False



 
    def add_session(self,session_id,username,expiry_time):

        query = "INSERT INTO Sessions (session_id,username,expiry_time) VALUES (?, ?, ?)"

        # print(sql_cmd)
        self.cur.execute(query, (session_id,username,expiry_time,))
        self.conn.commit()

        return True




    def retrieve_session_data(self,session_id):
        # Query the session data store to retrieve the session data associated with the session ID
        query= "SELECT * FROM Sessions WHERE session_id = ? "
        self.cur.execute(query,(session_id,))
        row = self.cur.fetchone()
        if row:
            # If the session data exists, return it as a dictionary
            session_data = {
                'session_id': row[0],
                'username': row[1],
                'expiry_time': row[2]
            }

            # print(row)

            return session_data
        else:
            # If the session data does not exist, return None
            return None
    


    def remove_session_data_by_session_id(self,session_id):
        self.cur.execute("DELETE FROM sessions WHERE session_id=?", (session_id,))

        # Commit the changes to the database and close the connection
        self.conn.commit()

    def remove_session_data_by_username(self,username):
        self.cur.execute("DELETE FROM sessions WHERE username=?", (username,))

        # Commit the changes to the database and close the connection
        self.conn.commit()

    def update_session_data(self,session_id, session_data):

        self.cur.execute('UPDATE sessions SET username = ?, expiry_time = ? WHERE session_id = ?',(session_data['username'], session_data['expiry_time'], session_id,))
        self.conn.commit()









