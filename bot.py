# This code was facelifted from: https://github.com/yashar1/reddit-comment-bot
import config
import os
import praw  # 3rd party package
import re
import time

REDDIT_CLIENT = None

COMMENT_REPLY_BODY = '''
Ararat is and remains Armenian. The Republic of Turkiye must recognize the cultural significance of
Mount Ararat to the Armenian people.

Please share: https://freeararat.com


I am a bot. You can find my source code [here](https://github.com/naltun/freeararat).
'''


def bot_login() -> praw.Reddit:
    global REDDIT_CLIENT
    print('[*] Logging in...')
    REDDIT_CLIENT = praw.Reddit(
        username=config.username,
        password=config.password,
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent='linux:freeararat:0.1.0 (by u/freeararat)',
    )
    print('[*] Logged in')


def get_saved_comments() -> list:
    if not os.path.isfile('comments_replied_to.txt'):
        comments_replied_to = []
    else:
        with open('comments_replied_to.txt', 'r') as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split('\n')
            comments_replied_to = list(filter(None, comments_replied_to))
    return comments_replied_to


def run_bot(reddit, comments_replied_to) -> None:
    print('[*] Searching last 500 comments...')
    for comment in reddit.subreddit('armenia').comments(limit=500):
        if (
            ('Ararat' in comment.body or 'ararat' in comment.body)
            and comment.id not in comments_replied_to
            and comment.author != reddit.user.me()
        ):
            print(f'[!] Comment found! Replying to comment {comment.id}')
            comment.reply(COMMENT_REPLY_BODY)
            print(f'[!] Replied to {comment.id}!')
            comments_replied_to.append(comment.id)
            with open('comments_replied_to.txt', 'a') as f:
                f.write(f'{comment.id}\n')
    print('[*] Search complete. Sleeping for 30 minutes...')
    time.sleep(60 * 30)  # 60s * 30m


def run() -> None:
    bot_login()
    comments = get_saved_comments()
    run_bot(REDDIT_CLIENT, comments)


if __name__ == '__main__':
    try:
        run()
    except praw.exceptions.RedditAPIException as e:
        sleep_time = int(re.findall(r'break for (\d) minute', str(e))[0])
        print(f'[!] Rate limit exceeded, sleeping for {sleep_time} minutes...')
        time.sleep(60 * sleep_time)  # 60s * sleep_time as minutes
        if not REDDIT_CLIENT:
            bot_login()
        comments = get_saved_comments()
        run_bot(REDDIT_CLIENT, comments)
