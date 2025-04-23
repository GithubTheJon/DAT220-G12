from flask import Flask, render_template, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey123"

def get_data(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT posts.post_id, users.username, posts.content,
            (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.post_id) as like_count
        FROM posts
        JOIN users ON posts.user_id = users.user_id
        ORDER BY posts.created_at DESC
    """)
    posts = cursor.fetchall()

    cursor.execute("""
        SELECT comments.post_id, users.username, comments.content
        FROM comments
        JOIN users ON comments.user_id = users.user_id
        ORDER BY comments.created_at ASC
    """)
    all_comments = cursor.fetchall()
    comments_by_post = {}
    for post_id, commenter, content in all_comments:
        comments_by_post.setdefault(post_id, []).append({'username': commenter, 'content': content})

    liked_post_ids = set()
    if user_id:
        cursor.execute("SELECT post_id FROM likes WHERE user_id = ?", (user_id,))
        liked_post_ids = set(row[0] for row in cursor.fetchall())

    conn.close()
    return posts, comments_by_post, liked_post_ids


@app.route("/")
def index():
    session["user_id"] = 1
    user_id = session["user_id"]
    posts, comments_by_post, liked_post_ids = get_data(user_id)
    return render_template("index.html", posts=posts,
                           comments_by_post=comments_by_post,
                           liked_post_ids=liked_post_ids,
                           user_id=user_id)


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


@app.route("/like/<int:post_id>", methods=["POST"])
def like_post(post_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to like posts.")
        return redirect(url_for("index"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("INSERT INTO likes (post_id, user_id) VALUES (?, ?)", (post_id, user_id))
    conn.commit()
    
    conn.close()
    return redirect(url_for("index"))


@app.route("/unlike/<int:post_id>", methods=["POST"])
def unlike_post(post_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to unlike posts.")
        return redirect(url_for("index"))

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM likes WHERE post_id = ? AND user_id = ?", (post_id, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__=="__main__":
    app.run(debug=True, port=9091)
    