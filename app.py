from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key ='InternA7coder'
# Create a MySQL connection
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='test'
)

# Create the "words" table if it doesn't exist
create_table_query = '''
    CREATE TABLE IF NOT EXISTS words (
        id INT AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(255) NOT NULL
    )
'''
with connection.cursor() as cursor:
    cursor.execute(create_table_query)
    connection.commit()

# Insert a sample word if the table is empty
insert_word_query = '''
    INSERT INTO words (word) SELECT * FROM (SELECT 'Test') AS tmp
    WHERE NOT EXISTS (SELECT * FROM words)
'''
with connection.cursor() as cursor:
    cursor.execute(insert_word_query)
    connection.commit()


@app.route('/', methods=['GET'])
def get_word():
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT word FROM words LIMIT 1')
        result = cursor.fetchone()
        if result:
            word = result[0]
            return jsonify({'word': word})
        else:
            return jsonify({'error': 'No word found in the database'})
    except mysql.connector.Error as error:
        print('Error querying the database:', error)
        return jsonify({'error': 'Failed to fetch the word from the database'})

# **************************Admin Route**************************

@app.route('/admin', methods=['GET', 'POST'])
def admin_portal():
    if 'username' in session:
        if request.method == 'POST':
            
            try:
                new_word = request.form['word']
                cursor = connection.cursor()
                cursor.execute('UPDATE words SET word = %s LIMIT 1', (new_word,))
                connection.commit()
               
                return render_template('admin.html', message='Word updated successfully')
            except mysql.connector.Error as error:
                print('Error updating the word in the database:', error)
                return render_template('admin.html', message='Failed to update the word')
        return render_template('admin.html', message='')
    else:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            # Perform admin authentication here (e.g., check username and password against stored credentials)
            if username == 'admin' and password == 'root':
                session['username'] = username
               
                return redirect(url_for('admin_portal'))
            else:
                return render_template('admin.html', message='Invalid username or password')
        return render_template('admin.html')

if __name__ == '__main__':
    app.run()
