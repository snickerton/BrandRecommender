import selenium
from googlesearch import search
import praw



query = "best shoes reddit"
threads = search(query, num=10, start=0, stop=10, pause=2)
# print(list(threads))

reddit = praw.Reddit(client_id='my client id',
                     client_secret='my client secret',
                     user_agent='my user agent')
for t in threads:
    print(t)
    submission = reddit.submission(url=t)
    print(submission)
    for top_level_comment in submission.comments:
        print(top_level_comment.body)

print("done")