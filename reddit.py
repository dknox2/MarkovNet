import praw

reddit = praw.Reddit(
    client_id="-uOTtsomz9tUbw",
    client_secret="TUQv9XGl8nyylcpqC-Q87dNjnUE",
    user_agent="knowledge_dragon"
)

ask_reddit = reddit.subreddit("askreddit")

top_posts = ask_reddit.top(time_filter="all", limit=1000)

questions = []
for post in top_posts:
    questions.append(post.title)

with open("askreddit_top.txt", "w") as output:
    for question in questions:
        print(question, file=output)