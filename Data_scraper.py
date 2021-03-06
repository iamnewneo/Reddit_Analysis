
# coding: utf-8

# In[129]:

import praw
# import warnings
# warnings.filterwarnings('ignore')
import warnings

def fxn():
    warnings.warn("deprecated", DeprecationWarning)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    fxn()

# In[130]:

from pprint import pprint


# In[131]:

import sqlite3 as sqlite


# In[132]:

conn = sqlite.connect('television_database.db')
c = conn.cursor()


# In[133]:

c.execute('''CREATE TABLE IF NOT EXISTS subreddits
             (subId text, postId text)''')
c.execute('''CREATE TABLE IF NOT EXISTS posts
             (postId text, postTitle text, postText text, postTime text, postUpvote text, totalComments text)''')
c.execute('''CREATE TABLE IF NOT EXISTS comments
             (postId text, commentId text, commentText text, commentTime text, commentUpvotes text)''')


# In[134]:

r = praw.Reddit(user_agent="Reddit Analysis Script")


# In[135]:

# username = "r3ddit3rs"
# password = "redditanalysis"


# In[136]:

# r.login(username, password)


# In[137]:

subreddit = r.get_subreddit('television')
posts = subreddit.get_top_from_all(limit=1000)
posts_ids = []
for post in posts:
    posts_ids.append(post.id)
print("Toal number of posts")
print(len(posts_ids))
# In[138]:
count = 0
for posts_id in posts_ids:
    try:
        subreddit_id = subreddit.id
        submission = r.get_submission(submission_id=posts_id)
        submission.replace_more_comments(limit=None, threshold=0)
        comments = praw.helpers.flatten_tree(submission.comments)
    except:
        print("Error fetching data for submission id: " + str(posts_id))
    try:
        submission_id = submission.id
    except:
        submission_id = str(999999)
    try:
        submission_title = submission.title
    except:
        submission_title = str(999999)
    try:
        submission_text = submission.selftext
    except:
        submission_text = str(999999)
    try:
        submission_created_at = submission.created_utc
    except:
        submission_created_at = str(999999)
    try:
        submission_ups = submission.ups
    except:
        submission_ups = str(999999)
    try:
        submission_total_comments = submission.num_comments
    except:
        submission_total_comments = str(999999)
    try:
        c.execute("INSERT INTO subreddits VALUES (?, ?)", (subreddit_id, submission_id))
        c.execute("INSERT INTO posts VALUES (?, ?, ?, ?, ?, ?)",
                  (submission_id, submission_title, submission_text, submission_created_at, submission_ups, submission_total_comments))
    except:
        print("..................SQL ERROR...........")
    #print(submission_id, submission_text, submission_created_at, submission_ups, submission_total_comments)
    for comment in comments:
        try:
            comment_id = comment.id
        except:
            comment_id = str(999999)
        try:
            comment_body = comment.body
        except:
            comment_body = str(999999)
        try:
            comment_created_at = comment.created_utc
        except:
            comment_created_at = str(999999)
        try:
            comment_ups = comment.ups
        except:
            comment_ups = str(999999)
        try:
            c.execute("INSERT INTO comments VALUES (?, ?, ?, ?,?)",
                      (submission_id,comment_id, comment_body, comment_created_at, comment_ups))
        except:
            print("..................SQL ERROR...........")
        #print(submission_id,comment_id, comment_body, comment_created_at, comment_ups)
    count = count + 1
    conn.commit()
    print("Total " + str(count) + " submissions scraped.")


# In[139]:

conn.commit()
conn.close()


# In[ ]:



