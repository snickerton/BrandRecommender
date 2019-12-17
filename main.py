import selenium
from googlesearch import search
import praw
import json
from praw.models import MoreComments
from collections import Counter
from nltk.tag import pos_tag
import re


# Initialize reddit
with open('nukeCodes.txt', 'r') as file:
    nukeCodes = json.load(file)

CLIENT_SECRET = nukeCodes['secret']
CLIENT_ID = nukeCodes['id']

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent='Brand Recommender')


# Google
item = input("Enter an item (e.g. \"shoes\"): ")
# item = "shoes"
query = "best " + item + " reddit"
threads = list(search(query, num=10, start=0, stop=10, pause=2))
print(threads)

threads = [x for x in threads if 'comments' in x.split('/')]
print(threads)
num_comments = 3

final_wordlist = []

for t in threads:

    print("\n\n"+t)
    submission = reddit.submission(url=t)
    submission.comments.replace_more()

    print("Score: ", submission.score)
    print("\n")

    if(len(submission.selftext) > 1000):
        # if the body of the submission is huge it's probably a guide/post not a question asking for recs
        # Alternatively: if(submission.title contains "guide")
        print("Guide: ")
        print(submission.selftext)
        # split by anything whitespace
        final_wordlist.extend(submission.selftext.split())
        #might need to post the comments if some unorthodox thing is happening (shoes thread)
    else:
        comments = submission.comments.list()
        comments = sorted(comments, key=lambda a: a.score, reverse=True)
        comments = [x for x in comments if x.parent_id == x.link_id]
        print("Here are the top ",num_comments," comments:")
        # print out the comment recommendations
        num_comments = min(num_comments,len(comments))
        for x in range(num_comments):
            # print("*************** Comment  | Score: ", c.score, "***************")
            # print("\n\n")
            # print(c.body)

            print("*************** Comment #", x+1, " | Score: ", comments[x].score,"***************")
            print("\n")
            print(comments[x].body)
            final_wordlist.extend(comments[x].body.split())

print("Final frequency chart:")
most_freq_words = Counter(final_wordlist)
ignore= ['the','The','be','this','at','have','can','more','will','a','if','in','it','of','or','and','to','for','you','are','I','on','that','-','with','is','*','but','as','not','most','like','your', ".", "|","___"]
for word in ignore:
    if word in most_freq_words:
        del most_freq_words[word]
print(most_freq_words.most_common(30))

# list of links in order of appearance (top google search, then top comment)
links_from_comments = []

for x in final_wordlist:
    # reddit often formats links like such: [text](link)
    # searching for ]( might also work but not everyone formats their links, some just paste a raw text
    if "http" in x and ("reddit" not in x and "redd.it" not in x and "imgur" not in x):
        # we substring from between the parenthesis of [text](link) and just hope that they put spaces if they didn't try to format
        links_from_comments.append(x[x.find('(')+1:x.find(')')])

print("Links found in comments: ")
print(links_from_comments)

print("done")