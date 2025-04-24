import sqlite3
from sqlite3 import Error

database = r"./database.db"

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


sql_create_users_table = """CREATE TABLE IF NOT EXISTS users (
                                user_id INTEGER PRIMARY KEY,
                                username TEXT NOT NULL,
                                intrests TEXT
                            );"""
                            
sql_create_posts_table = """CREATE TABLE IF NOT EXISTS posts (
                                post_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id NOT NULL,
                                content TEXT,
                                likes INT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users (user_id)
                            );"""
                            
sql_create_comments_table = """CREATE TABLE IF NOT EXISTS comments (
                                comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                post_id NOT NULL,
                                user_id NOT NULL,
                                content TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                FOREIGN KEY (user_id) REFERENCES users (user_id),
                                FOREIGN KEY (post_id) REFERENCES Posts(post_id)
                            );"""
                            
sql_create_likes_table = """CREATE TABLE IF NOT EXISTS likes (
                                like_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                post_id NOT NULL,
                                user_id NOT NULL,
                                FOREIGN KEY (user_id) REFERENCES users (user_id),
                                FOREIGN KEY (post_id) REFERENCES posts (post_id)
                                UNIQUE (user_id, post_id)
                            );"""               
                            
sql_create_followers_table = """CREATE TABLE IF NOT EXISTS followers (
                                follower_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user1_id NOT NULL,
                                user2_id NOT NULL,
                                FOREIGN KEY (user1_id) REFERENCES users (user_id),
                                FOREIGN KEY (user2_id) REFERENCES users (user_id)
                                UNIQUE (user1_id, user2_id)
                            );"""                                                                  
                            
def create_table(conn, create_tables_sql):
    try:
        c = conn.cursor()
        c.execute(create_tables_sql)
    except Error as e:
        print(e)
        
        
def setup():
    conn = create_connection(database)
    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_posts_table)
        create_table(conn, sql_create_comments_table)
        create_table(conn, sql_create_likes_table)
        create_table(conn, sql_create_followers_table)
        conn.close()
        

"""
# Get all the posts of a user
SELECT Posts.post_id, Posts.content, Users.username, Posts.created_at
FROM Posts
JOIN Users ON Posts.user_id = Users.user_id
ORDER BY Posts.created_at DESC;

# Get all the comments on a post
SELECT Comments.comment_text, Users.username, Comments.created_at
FROM Comments
JOIN Users ON Comments.user_id = Users.user_id
WHERE Comments.post_id = 1
ORDER BY Comments.created_at ASC;

# Get username of all who have liked the post
SELECT Users.username
FROM Likes
JOIN Users ON Likes.user_id = Users.user_id
WHERE Likes.post_id = 1;    #1 = current/clicked on 
"""

if __name__ == '__main__':
    setup()