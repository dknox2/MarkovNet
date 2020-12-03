import json
import pathlib

def parse_yearly_dump(year):
    total_posts = 0
    for i in range(1, 13):
        post_titles = []
        file_number = str(i).zfill(2)
        filename = pathlib.Path(__file__).parents[1] / "data" / "reddit_dumps" / ("RS_v2_" + year + "-" + file_number)
        if not filename.is_file():
            filename = pathlib.Path(__file__).parents[1] / "data" / "reddit_dumps" / ("RS_" + year + "-" + file_number)
        if not filename.is_file():
            continue

        with open(filename, encoding="utf-8") as file:
            for line in file:
                data = json.loads(line)
                subreddit = data["subreddit"]
                if subreddit.lower() == "askreddit":
                    title = data["title"]
                    post_titles.append(title)
    
        with open(pathlib.Path(__file__).parents[1] / "data" / "askreddit_posts" / year + "-" + file_number + ".txt", "w", encoding="utf-8") as file:
            for title in post_titles:
                print(title, file=file)
            total_posts += len(post_titles)

    print("found and saved", total_posts, "post titles")

if __name__ == "__main__":
    (pathlib.Path(__file__).parents[1] / "data" / "askreddit_posts").mkdir(parents=True, exist_ok=True)
    parse_yearly_dump("2019")