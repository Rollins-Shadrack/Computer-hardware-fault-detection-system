import tkinter as tk
import mysql.connector

# Create the GUI window
root = tk.Tk()
root.title('Login Page')
def authenticate():
    try:
        # Get the input from the username and password entry boxes
        username = username_entry.get()
        password = password_entry.get()

        # Connect to the MySQL database
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='rollins/2023',
            database='pest_control'
        )

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Execute the SQL query to retrieve the user with the given username and password
        query = 'SELECT * FROM users WHERE username = %s AND password = %s'
        values = (username, password)
        cursor.execute(query, values)

        # Check if the user exists in the database
        user = cursor.fetchone()
        if user:
            # If user exists, remove the login widgets and display the issue input box
            username_label.pack_forget()
            username_entry.pack_forget()
            password_label.pack_forget()
            password_entry.pack_forget()
            login_button.pack_forget()
            register_button.pack_forget()
            issue_label.pack()
            issue_entry.pack()
        else:
            # If user does not exist, display an error message
            welcome_label.config(text='Invalid username or password.')
    except mysql.connector.Error as error:
        # If there is a MySQL error, display the error message
        welcome_label.config(text='Error: {}'.format(error))


def show_register_page():
    # Remove the login widgets and display the registration widgets
    welcome_label.config(text='Welcome to the Registration Page!')
    username_label.pack_forget()
    username_entry.pack_forget()
    password_label.pack_forget()
    password_entry.pack_forget()
    login_button.pack_forget()
    register_button.pack_forget()
    issue_label.pack_forget()
    issue_entry.pack_forget()

    register_username_label.pack()
    register_username_entry.pack()
    register_password_label.pack()
    register_password_entry.pack()
    register_button2.pack()

def show_login_page():
    # Remove the registration widgets and display the login widgets
    welcome_label.config(text='Welcome to the Login Page!')
    register_username_label.pack_forget()
    register_username_entry.pack_forget()
    register_password_label.pack_forget()
    register_password_entry.pack_forget()
    register_button2.pack_forget()
    login_button.pack_forget()
    register_button.pack_forget()
    login_page_button.pack_forget()

    username_label.pack()
    username_entry.pack()
    password_label.pack()
    password_entry.pack()
    login_button.pack()
    register_button.pack()

def register():
    # Get the input from the registration entry boxes
    username = register_username_entry.get()
    password = register_password_entry.get()
    # Connect to the MySQL database
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='rollins/2023',
        database='pest_control'
    )

    # Create a cursor object to execute SQL queries
    cursor = db.cursor()

    # Execute the SQL query to insert the new user into the database
    query = 'INSERT INTO users (username, password) VALUES (%s, %s)'
    values = (username, password)
    cursor.execute(query, values)

    # Commit the changes to the database
    db.commit()

    # Clear the input boxes and display a success message
    register_username_entry.delete(0, tk.END)
    register_password_entry.delete(0, tk.END)
    welcome_label.config(text='Registration successful! You can now login.')

    # Close the database connection
    cursor.close()
    db.close()



# Create the welcome label
welcome_label = tk.Label(root, text='Welcome to the Login Page!')
welcome_label.pack(padx=5, pady=10)


# Create the 'Login Page' button to navigate to the login page
login_page_button = tk.Button(root, text='Login Page', command=show_login_page)
login_page_button.pack(padx=5, pady=6)


# Create the 'Register' button to navigate to the registration page
register_button = tk.Button(root, text='Register', command=show_register_page)
register_button.pack(padx=5, pady=6)

# Create the input box for knowing which hardware has an issue
issue_label = tk.Label(root, text='Do you know which computer hardware has a problem? (Yes/No):')
issue_entry = tk.Entry(root, width=50)

# Create the registration page widgets
register_username_label = tk.Label(root, text='Enter a username:')
register_username_entry = tk.Entry(root, width=50)
register_password_label = tk.Label(root, text='Enter a password:')
register_password_entry = tk.Entry(root, width=50, show='*')
register_button2 = tk.Button(root, text='Register', command=register)

# Create the input box for username
username_label = tk.Label(root, text='Username:')
username_entry = tk.Entry(root, width=50)
password_label = tk.Label(root, text='Password:')
password_entry = tk.Entry(root, width=50, show='*')
login_button = tk.Button(root, text='Login', command=authenticate)
#Run the main loop of the GUI
root.mainloop()

