# redditFlairDetection
link - https://precog-reddit.herokuapp.com/ <br>
# The Project
The dependencies are present in requirements.txt<br>
getReddit.py was used to scrap the data from r/india and populate the database which was hosted on MongoDB atlas. The subreddit was searched for all the mentioned flairs and then they were added to the database.This can be used by running python3 getreddit.py <br>
Jupyter notebook was used to check the models for the prototyping phase. The file classify.py has all the classifiers tested and their accuracy along with them. 4 classifiers with different feature set were tested. This can be used by running classify.py on a jupyter notebook.About 1500 posts were finally used for training and testing. All flairs had at least 100 posts in the database. <br>
For the last part of the project I used flask to host the webapp.The application is currently hosted on heroku. The project can be hosted on localhost by running python3 app.py in a system with flask and all the dependencies mentioned in the requirements.txt installed. It runs on port 5000.<br>
# Some Results 
MultinomialNB with titles - accuracy 0.5809716599190283 <br>
SGDClassifier with titles - accuracy 0.6538461538461539 <br>
LogisticRegression with titles - accuracy 0.6396761133603239 <br>
