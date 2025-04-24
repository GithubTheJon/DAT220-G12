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
    (1, "I like trains!"),
    (2, "To be or not to be..."),
    (3, "P00P"),
    (1, "Had Pineapple on Pizza for dinner today!"),
    (1, "Drinking tea while watching TV"),
    
    (3, "SIGMA"),
    (10, "ALIENS BUILDT A PIRAMID IN MY BACKYARD!!1"),
    (7, "Gaming at 12am today"),
    (9, "Fighting bears are scary man"),
    (5, "Baby hit me one more time! yeah! yeah!")
]


#ID, Likes, Content
comments = [
    (3, 6, "PP"),
    (3, 6, "PePe"),
    (6, 10,"Take me home to the country road!"),
    (4, 5, "Good lord"),
    (1, 1, "Liked my own post... SO WHAT!"),
    (2, 6, "Kongler"),
    
    (5, 7,"I love this"),
    (6, 8,"papa no more"),
    (7, 9,"Keep it up!"),
    (8, 5,"omg smh, brb"),
    (9, 4,"LOL")
    (2, 4,"LOL")
    (5, 4,"LOL")
]

likes = [
    (7, 9),
    (4, 9),
    (3, 9),
    (2, 9),
    
    (9, 8),
    (8, 8),
    (7, 8),
    (6, 8),
    (5, 8),
    (4, 8),
    (3, 8),
    (2, 8),
    (1, 8),
    
    (9, 7),
    (8, 7),
    (7, 7),
    (6, 7),
    (5, 7),
    (4, 7),
    (3, 7),
    (2, 7),
    (1, 7),
    
    (9, 6),
    (8, 6),
    (6, 6),
    (5, 6),
    (1, 6),
    
    (2, 5),
    (8, 5),
    (7, 5),
    (3, 5),
    
    (9, 4),
    (8, 4),
    (7, 4),
    (3, 4),
    
    (9, 3),
    (8, 3),
    (6, 3),
    (3, 3),
    
    (5, 2),
    (7, 2),
    (6, 2),
    (3, 2)

]

followers = [
    (8,1),
    (1,6),
    (1,7),
    (1,8),
    (1,9),
    (2,8),
    (2,9),
    (3,8),
    (4,7),
    (5,6),
    (6,5),
    (7,4),
    (8,3),
    (9,2),
    (4,1)
]

def insert_data():
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()

        # Insert users
        cursor.executemany("INSERT INTO users (username, intrests, followers) VALUES (?, ?, ?)", users)
        conn.commit()
        print("users inserted successfully!")
        
        cursor.executemany("INSERT INTO posts (user_id, content) VALUES (?, ?)", posts)
        conn.commit()
        print("posts inserted successfully!")
        
        cursor.executemany("INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)", comments)
        conn.commit()
        print("comments inserted successfully!")
        
        cursor.executemany("INSERT INTO likes (post_id, user_id) VALUES (?, ?)", likes)
        conn.commit()
        print("likes inserted successfully!")
        
        cursor.executemany("INSERT INTO followers (user1_id, user2_id) VALUES (?, ?)", followers)
        conn.commit()
        print("followers inserted successfully!")
    
    
    except sqlite3.Error as e:
        print("SQLite error:", e)
    
    finally:
        conn.close()


if __name__ == "__main__":
    insert_data()
