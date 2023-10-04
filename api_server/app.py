from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data['username']
    password = data['password']
    user_data = data.get('data', '')
    rights = data.get('rights', '')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, password, data, rights) VALUES (?, ?, ?, ?)', (username, password, user_data, rights))
    conn.commit()
    conn.close()

    return jsonify({"message": "User created successfully!"}), 201

# ... [Autres routes pour récupérer, mettre à jour, et supprimer des utilisateurs]

if __name__ == '__main__':
    app.run(debug=True)
