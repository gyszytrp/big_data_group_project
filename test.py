import sqlite3

# Create a connection to the database
conn = sqlite3.connect('temp.db')
c = conn.cursor()

# Define a SQL query with a placeholder for a value
query = "SELECT * FROM User WHERE username = ? and password= ? "

# Execute the query with user input as a parameter
user_input = 'a'
pwd="q"
c.execute(query, (user_input,pwd,))

# Fetch the results of the query
results = c.fetchall()

# Do something with the results
for row in results:
    print(row)

# Close the database connection
conn.close()
