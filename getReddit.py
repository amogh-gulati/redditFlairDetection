import praw
from pymongo import MongoClient
import dns

reddit = praw.Reddit(client_id='4p5HvasxFSLoZA',
                client_secret='1jXUIrXjjIsF7EZL0JmCPiTeKvI',
                user_agent='precog by u/amogh7777 github : amogh-gulati')



subreddit = reddit.subreddit('india')


print(subreddit.display_name)  # Output: redditdev
#print(subreddit.title)         # Output: reddit Development
#print(subreddit.description)   # Output: A subreddit for discussion of ...

flairs = [        'Demonetization', 'Policy & Economy', 'Science & Technology', 'Entertainment', 'Year In Review', 'AMA', '*First Indian Woman', 'Food', 
        'Misleading', 'hmmm', 'Policy', 'Casual AMA 9¾/10', '| Low-effort Self Post |', 'Politics [OLD]', 'Net Neutrality', 'Governance',None,'None','Unverified', 'AskIndia', 'Non-Political', '[R]eddiquette', 'Politics', 'Flair about post flairs', 'Policy/Economy', 'Photography',
         'Askindia', 'Business/Finance', 'Well played, OP!', 'Casual', 'Sports', 'Technology', 'Scheduled', 'Science/Technology', 'Launch Successful']

count_posts = {}
for x in flairs:
        count_posts[x] = 0

data = []
data_ids = []

for flair in flairs:
        submissions = subreddit.search(flair,limit = None)
        count = 0
        for submission in submissions:
                print("meh")
                # print(submission.selftext)
                if submission.link_flair_text not in flairs:
                        print("error")
                        print(submission.link_flair_text)
                if submission.id not in data_ids and submission.link_flair_text in flairs:
                        if submission.link_flair_text==None:
                                submission.link_flair_text = 'None'
                        data.append(submission)
                        data_ids.append(submission.id)
                        count_posts[''+submission.link_flair_text] = count_posts[''+submission.link_flair_text] + 1
                         
# for submission in subreddit.hot():
#         if submission.link_flair_text not in flairs:
#                 print("error")
#                 print(submission.link_flair_text)
#         if submission.id not in data_ids and submission.link_flair_text in flairs:
#                 if submission.link_flair_text==None:
#                         submission.link_flair_text = 'None'
#                 data.append(submission)
#                 data_ids.append(submission.id)
#                 count_posts[''+submission.link_flair_text] = count_posts[''+submission.link_flair_text] + 1

for x in flairs:
        print(x,count_posts[x])

exit()
post_data = []
for submission in data:
        print(submission.title)
        post = {}
        post['upvote_ratio'] = submission.upvote_ratio
        post['name'] = submission.name
        post['title'] = submission.title
        post['score'] = submission.score
        post['id'] = submission.id
        post['url'] = submission.url
        post['flair'] = submission.link_flair_text
        post['com_count'] = submission.num_comments
        post['self_text'] = submission.selftext
        post_data.append(post)


client = MongoClient("mongodb+srv://amogh:onetwothree@precogreddit-k1wz2.mongodb.net/test?retryWrites=true&w=majority")
db = client['precogReddit']
collection = db['reddit_india2']
ret = collection.insert_many(post_data)
print(ret)