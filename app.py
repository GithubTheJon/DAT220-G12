from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def get_data():
    conn = sqlite3.connect("database.db")  # Replace with your actual database file
    cursor = conn.cursor()
    
    # Corrected query: Fetch username instead of user_id
    cursor.execute("""
        SELECT users.username, posts.content, posts.likes
        FROM posts
        INNER JOIN users ON posts.user_id = users.user_id
        ORDER BY posts.created_at DESC;
    """)
    
    data = cursor.fetchall()  # Fetch all posts
    columns = ["Username", "Content", "Likes"]  # Define correct column headers
    conn.close()
    
    return columns, data



@app.route("/")
def index():
    columns, data = get_data()
    return render_template('index.html', columns=columns, data=data)


@app.route("/user/<string:username>/")
def user_page(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Fetch the user's posts
    cursor.execute("""
        SELECT posts.content, posts.likes
        FROM posts
        JOIN users ON posts.user_id = users.user_id
        WHERE users.username = ?;
    """, (username,))
    
    user_posts = cursor.fetchall()
    conn.close()

    return render_template('user_page.html', username=username, user_posts=user_posts)

if __name__=="__main__":
    app.run(debug=True, port=9091)
    