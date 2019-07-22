from flask import Flask , render_template,request
 
import praw
from pymongo import MongoClient
import pandas as pd
import numpy as np
from numpy import random    
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import re
from sklearn.metrics import accuracy_score, confusion_matrix
#import gensim
import nltk
from nltk.corpus import stopwords
from sklearn.linear_model import LogisticRegression
import dns
import random
#%matplotlib inline

classifiers = {}

# def cleanText(text):
#     return text
def cleanText(text):
    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
    STOPWORDS = set(stopwords.words('english'))
    text = text.lower() # lowercase text
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join(word for word in text.split() if word not in STOPWORDS) # delete stopwors from text
    return text

def predictPost(content,classifier):
    try:
        reddit = praw.Reddit(client_id='4p5HvasxFSLoZA',
        client_secret='1jXUIrXjjIsF7EZL0JmCPiTeKvI',
        user_agent='precog by u/amogh7777 github : amogh-gulati')
        submission = reddit.submission(url=content)
        print(submission)
    except:
        print("url not in the right format")
        return None
    if classifiers=={}:
        train()
    y_pred = None
    print(content)
    print(classifier)
    print(classifiers.keys())
    if classifier not in classifiers.keys():
        print("no such model found")
    else:
        if classifier[1]=='titex':
            titex = []
            titex.append(cleanText(submission.name)+cleanText(submission.selftext))
            y_pred = classifiers[classifier].predict(titex)
            print(y_pred)
            print(submission.link_flair_text)
        elif classifier[1]=='titles':
            title = []
            title.append(cleanText(submission.title))
            y_pred = classifiers[classifier].predict(title)
            print(y_pred)
            print(submission.link_flair_text)
        elif classifier[1]=='text':
            text = []
            text.append(cleanText(submission.selftext))
            y_pred = classifiers[classifier].predict(text)
            print(y_pred)
            print(submission.link_flair_text)
        elif classifier[1]=='urls':
            url = []
            url.append(cleanText(submission.url))
            y_pred = classifiers[classifier].predict(url)
            print(y_pred)
            print(submission.link_flair_text)
        elif classifier[1]=='mix':
            mix = []
            mix.append(cleanText(submission.title)+cleanText(submission.selftext)+cleanText(submission.url))
            y_pred = classifiers[classifier].predict(mix)
            print(y_pred)
            print(submission.link_flair_text)
        else:
            print("no such feature")
        return y_pred

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result',methods=['POST','GET'])
def index2():
    if request.method == 'POST':
        print(request.form)
        content = request.form['redditurl']
        classifier = (request.form['classifier'],request.form['features'])
        y = predictPost(content,classifier)
        if y==None:
            y = ["The url was not in the correct format"]
        return render_template('index2.html',result  = [y[0] ,"link given :- " + content])
    else:
        return render_template('index.html')
def train():
    global classifiers
    classifiers = {}
    client = MongoClient("mongodb+srv://amogh:onetwothree@precogreddit-k1wz2.mongodb.net/test?retryWrites=true&w=majority")
    db = client['precogReddit'] 
    collection = db['reddit_india']
    results = collection.find({})
    print(results)
    flairs = ['Unverified', 'AskIndia', 'Non-Political', '[R]eddiquette', 'Politics', 'Flair about post flairs', 'Policy/Economy', 'Photography',
         'Askindia', 'Business/Finance', 'Well played, OP!', 'Casual', 'Sports', 'Technology', 'Scheduled', 'Science/Technology', 'Launch Successful',
        'Demonetization', 'Policy & Economy', 'Science & Technology', 'Entertainment', 'Year In Review', 'AMA', '*First Indian Woman', 'Food', 
        'Misleading', 'hmmm', 'Policy', 'Casual AMA 9¾/10', '| Low-effort Self Post |', 'Politics [OLD]', 'Net Neutrality', 'Governance']
    count_posts = {}
    for x in flairs:
            count_posts[x] = 0
    bigg_flairs = []
    for post in results:
        if post['flair'] not in flairs:
            pass
        else:
            count_posts[post['flair']] = count_posts[post['flair']] + 1
    for x in flairs:
        if count_posts[x]>100:
            bigg_flairs.append(x)


    flares = []
    names = []
    titles = []
    scores = []
    text = []
    urls = []
    mix = []
    titex = []
    post_count = 0
    for x in flairs:
        count_posts[x] = 0
    results = collection.find({})
    for post in results:
        if post['flair'] in bigg_flairs and count_posts[post['flair']]<200:
            flares.append(post['flair'])
            names.append(cleanText(post['name']))
            titles.append(cleanText(post['title']))
            scores.append(post['score'])
            text.append(cleanText(post['self_text']))
            urls.append(cleanText(post['url']))
            mix.append(names[post_count]+titles[post_count]+str(scores[post_count])+text[post_count]+urls[post_count])
            titex.append(titles[post_count]+text[post_count])
            post_count = post_count + 1
            count_posts[post['flair']] = count_posts[post['flair']] + 1
    print(post_count)
    #X_train, X_test, y_train, y_test = train_test_split(titex, flares, test_size=0.0, random_state = 42)
    #-----------------------------------------------------------------------------------------------------------------------
    print("SGDClassifier training")
    
    classifiers[('SGDClassifier','titles')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
                ])
    classifiers[('SGDClassifier','titles')].fit(titles, flares)


    classifiers[('SGDClassifier','text')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
                ])
    classifiers[('SGDClassifier','text')].fit(text, flares)

    classifiers[('SGDClassifier','urls')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
                ])
    classifiers[('SGDClassifier','urls')].fit(urls, flares)

    
    classifiers[('SGDClassifier','mix')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
                ])
    classifiers[('SGDClassifier','mix')].fit(mix, flares)

    classifiers[('SGDClassifier','titex')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42, max_iter=5, tol=None)),
                ])
    classifiers[('SGDClassifier','titex')].fit(titex, flares)
        #-----------------------------------------------------------------------------------------------------------------------
    print("MultinomialNB training")
    
    classifiers[('MultinomialNB','titles')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', MultinomialNB()),
                ])
    classifiers[('MultinomialNB','titles')].fit(titles, flares)


    classifiers[('MultinomialNB','text')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', MultinomialNB()),
                ])
    classifiers[('MultinomialNB','text')].fit(text, flares)

    classifiers[('MultinomialNB','urls')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', MultinomialNB()),
                ])
    classifiers[('MultinomialNB','urls')].fit(urls, flares)

    
    classifiers[('MultinomialNB','mix')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', MultinomialNB()),
                ])
    classifiers[('MultinomialNB','mix')].fit(mix, flares)

    classifiers[('MultinomialNB','titex')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', MultinomialNB()),
                ])
    classifiers[('MultinomialNB','titex')].fit(titex, flares)
    #-----------------------------------------------------------------------------------------------------------------------
    print("logistic regression training")
    
    classifiers[('LogisticRegression','titles')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf',  LogisticRegression(n_jobs=1, C=1e5)),
                ])
    classifiers[('LogisticRegression','titles')].fit(titles, flares)


    classifiers[('LogisticRegression','text')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', LogisticRegression(n_jobs=1, C=1e5)),
                ])
    classifiers[('LogisticRegression','text')].fit(text, flares)

    classifiers[('LogisticRegression','urls')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', LogisticRegression(n_jobs=1, C=1e5)),
                ])
    classifiers[('LogisticRegression','urls')].fit(urls, flares)

    
    classifiers[('LogisticRegression','mix')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', LogisticRegression(n_jobs=1, C=1e5)),
                ])
    classifiers[('LogisticRegression','mix')].fit(mix, flares)

    classifiers[('LogisticRegression','titex')] = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', LogisticRegression(n_jobs=1, C=1e5)),
                ])
    classifiers[('LogisticRegression','titex')].fit(titex, flares)
    print("model started")
if __name__ == "__main__" :
    train()
    app.run(debug=True)