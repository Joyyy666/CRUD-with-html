from flask import Flask,render_template, request, redirect 
import sqlite3

app = Flask(__name__)

def sql():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    return conn, cursor

@app.route('/')
def baca():
    # Ambil data dari database
    conn, cursor = sql()
    cursor.execute('SELECT * FROM user;')
    data = cursor.fetchall()
    conn.close()
    #print(data)
    return render_template('index.html', data=data)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn, cursor = sql()
        cursor.execute(f"INSERT INTO user (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        
        return redirect('/')
        
    else:
        return render_template('edit.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn, cursor = sql()
        cursor.execute("UPDATE user SET username=?, password=? WHERE id=?", (username, password, id))
        conn.commit()
        conn.close()
        
        return redirect('/')
    else:
        conn, cursor = sql()
        cursor.execute("SELECT * FROM user")
        tabel = cursor.fetchall()
        conn.close()
        #print(tabel[id-1][1])
        return render_template('edit.html', id=id, tabel=tabel)

@app.route('/hapus/<int:id>')
def hapus(id):
    conn, cursor = sql()
    cursor.execute(f"DELETE FROM user WHERE id=?", (id,))
    conn.commit()
    conn.close()
    
    return redirect('/')
    

if __name__ == '__main__':
    app.run(debug=True)