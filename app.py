from flask import Flask, render_template, redirect, url_for, session, flash, request
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey123"

def get_user_comments(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT posts.content, comments.content
        FROM comments
        JOIN posts ON comments.post_id = posts.post_id
        WHERE comments.user_id = ?;
    """, (user_id,))
    user_comments = cursor.fetchall()
    conn.close()
    return user_comments

def get_all_posts_with_likes():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
       SELECT posts.post_id, users.username, posts.content,
       (SELECT COUNT(*) FROM likes WHERE likes.post_id = posts.post_id),
       posts.user_id
        FROM posts
        JOIN users ON posts.user_id = users.user_id
        ORDER BY posts.created_at DESC
        """)
    posts = cursor.fetchall()
    conn.close()
    return posts

def get_all_comments_grouped_by_post():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        SELECT comments.post_id, comments.content, users.username
        FROM comments
        JOIN users ON comments.user_id = users.user_id
        ORDER BY comments.created_at ASC;
    """)
    rows = cur.fetchall()

    comments_by_post = {}
    for post_id, content, username in rows:
        comments_by_post.setdefault(post_id, []).append({
            'username': username,
            'content': content
        })
    conn.close()
    return comments_by_post


def get_user_likes(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT post_id FROM likes WHERE user_id = ?", (user_id,))
    liked_posts = {row[0] for row in cursor.fetchall()}
    conn.close()
    return liked_posts

def get_user_followers(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT users.username
        FROM followers
        JOIN users ON followers.user1_id = users.user_id
        WHERE followers.user2_id = ?
    """, (user_id,))
    followers = [row[0] for row in cursor.fetchall()]
    conn.close()
    return followers

@app.route("/")
def index():
    session["user_id"] = 1    
    user_id = session["user_id"]

    posts = get_all_posts_with_likes()
    comments_by_post = get_all_comments_grouped_by_post()
    liked_post_ids = get_user_likes(user_id)
    
    return render_template("index.html", posts=posts, comments_by_post=comments_by_post,
                           liked_post_ids=liked_post_ids, user_id=user_id)
    

@app.route("/user/<string:username>/")
def user_page(username):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    user_id = row[0]
    posts = get_all_posts_with_likes()
    user_comments = get_user_comments(user_id)
    followers = get_user_followers(user_id)

    user_posts = [post for post in posts if post[1] == username]

    return render_template("user_page.html",
                           username=username,
                           user_posts=user_posts,
                           user_comments=user_comments,
                           followers=followers)


@app.route("/unlike/<int:post_id>", methods=["POST"])
def unlike_post(post_id):
    user_id = session.get("user_id")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM likes WHERE post_id = ? AND user_id = ?", (post_id, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/like/<int:post_id>", methods=["POST"])
def like_post(post_id):
    user_id = session.get("user_id")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO likes (post_id, user_id) VALUES (?, ?)", (post_id, user_id))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/create_comment", methods=["POST"])
def create_comment():
    user_id = session.get("user_id")
    post_id = int(request.form.get("post_id"))  # Make sure this is an int
    content = request.form.get("content", "").strip()
    
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)",
                   (post_id, user_id, content))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/create_post", methods=["POST"])
def create_post():
    user_id = session.get("user_id")
    content = request.form.get("content", "").strip()

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO posts (user_id, content) VALUES (?, ?)", (user_id, content))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/delete_post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    user_id = session.get("user_id")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Ensure the post belongs to the current user
    cursor.execute("SELECT user_id FROM posts WHERE post_id = ?", (post_id,))
    row = cursor.fetchone()

    if row and row[0] == user_id:
        # Delete associated likes and comments first if you're not using ON DELETE CASCADE
        cursor.execute("DELETE FROM likes WHERE post_id = ?", (post_id,))
        cursor.execute("DELETE FROM comments WHERE post_id = ?", (post_id,))
        cursor.execute("DELETE FROM posts WHERE post_id = ?", (post_id,))
        conn.commit()
        flash("Post deleted.")

    conn.close()
    return redirect(url_for("index"))


@app.route("/edit_post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    user_id = session.get("user_id")
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":
        new_content = request.form.get("content", "").strip()
        # Optional: Add length or content validation
        cursor.execute("SELECT user_id FROM posts WHERE post_id = ?", (post_id,))
        row = cursor.fetchone()

        if row and row[0] == user_id:
            cursor.execute("UPDATE posts SET content = ? WHERE post_id = ?", (new_content, post_id))
            conn.commit()
            flash("Post updated.")

        conn.close()
        return redirect(url_for("index"))

    # GET method: render the form
    cursor.execute("SELECT content, user_id FROM posts WHERE post_id = ?", (post_id,))
    row = cursor.fetchone()
    conn.close()

    content = row[0]
    return render_template("edit_post.html", post_id=post_id, content=content)


if __name__ == "__main__":
    app.run(debug=True, port=9091)
