import sqlite3

database = "database.db"

# Sample user data
users = [
    ("Alice", "Music, Travel", 120),
    ("Bob", "Tech, Gaming", 250),
    ("Charlie", "Reading, Hiking", 39),
    ("Darwin Smith", "Work", 49),
    ("Dave Tailor", "Singing in the showers", 56),
    
    ("Ole Martin", "Student", 14),
    ("Michael Bergland", "Video games", 42),
    ("Tom Hankerchief", "Acting", 1192),
    ("Joe Robert", "Smoking", 723),
    ("Alex Bones", "Talking, Aliens", 221)
]

# Sample post data (likes)
posts = [
    (1, "I like trains!", 10),
    (2, "To be or not to be...", 32),
    (3, "P00P", 5),
    (1, "Had Pineapple on Pizza for dinner today!", 23),
    (1, "Drinking tea while watching TV", 19),
    
    (3, "SIGMA", 9),
    (10, "ALIENS BUILDT A PIRAMID IN MY BACKYARD!!1", 232),
    (7, "Gaming at 12am today", 9),
    (9, "Fighting bears are scary man", 431),
    (5, "Baby hit me one more time! yeah! yeah!", 304)
]

comments = [
    (3, 6, "PP"),
    (6, 10,"Take me home to the country road!"),
    (4, 4, "Good lord"),
    (1, 1,"Liked my own post... SO WHAT!"),
    (1, 1,""),
    
    (1, 1,""),
    (1, 1,""),
    (1, 1,""),
    (1, 1,""),
    (1, 1,"")
]

def insert_data():
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Insert users
        cursor.executemany("INSERT INTO users (username, intrests, followers) VALUES (?, ?, ?)", users)
        conn.commit()
        print("users inserted successfully!")
        
        cursor.executemany("INSERT INTO posts (user_id, content, likes) VALUES (?, ?, ?)", posts)
        conn.commit()
        print("posts inserted successfully!")
        
        cursor.executemany("INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)", comments)
        conn.commit()
        print("comments inserted successfully!")
    
    except sqlite3.Error as e:
        print("SQLite error:", e)
    
    finally:
        conn.close()


if __name__ == "__main__":
    insert_data()
