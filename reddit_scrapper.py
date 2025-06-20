import requests
from datetime import datetime


class RedditScraper:
    BASE_URL = "https://www.reddit.com"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (RedditScraper/1.0)"
    }

    def __init__(self, timeout=10):
        self.timeout = timeout
        self.permalink = self.search_megathread()  # auto-run

    def search_megathread(self, subreddit="developersIndia", query="Who's looking for work") -> str | None:
        """Search subreddit for current month's megathread post and return permalink"""
        month_year = datetime.now().strftime("%B %Y").lower()
        url = f"{self.BASE_URL}/r/{subreddit}/search.json"
        params = {
            "q": query,
            "restrict_sr": "on",
            "sort": "new",
            "limit": 15
        }

        try:
            res = requests.get(url, headers=self.HEADERS, params=params, timeout=self.timeout)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            print(f"Error searching subreddit: {e}")
            return None

        for post in data.get("data", {}).get("children", []):
            title = post["data"].get("title", "").lower()
            if "monthly megathread" in title and month_year in title:
                print("✅ Found:", title)
                return post["data"]["permalink"]

        print("❌ No matching megathread found.")
        return None

    def fetch_post(self, permalink: str = None) -> dict | None:
        """Fetch post and top-level comments"""
        if permalink is None:
            permalink = self.permalink
        if not permalink:
            print("No permalink found.")
            return None

        full_url = f"{self.BASE_URL}{permalink}.json"

        try:
            res = requests.get(full_url, headers=self.HEADERS, timeout=self.timeout)
            res.raise_for_status()
            data = res.json()
        except Exception as e:
            print(f"Error fetching Reddit post: {e}")
            return None

        if not isinstance(data, list) or len(data) < 2:
            print("Unexpected Reddit JSON structure")
            return None

        post_data = data[0]["data"]["children"][0]["data"]
        title = post_data.get("title", "[no title]")
        body = post_data.get("selftext", "")
        comments_data = data[1]["data"]["children"]
        comments = self._extract_comments(comments_data)

        return {
            "title": title,
            "body": body,
            "comments": comments
        }

    def _extract_comments(self, children: list) -> list:
        comments = []
        for item in children:
            if item.get("kind") != "t1":
                continue
            comment = item.get("data", {})
            if comment.get("body") and comment.get("author") != "[deleted]":
                comments.append({
                    "author": comment.get("author"),
                    "score": comment.get("score", 0),
                    "body": comment.get("body")
                })
        return comments


# # === Usage ===
# if __name__ == "__main__":
#     scraper = RedditScraper()

#     # Automatically searched permalink
#     if scraper.permalink:
#         post = scraper.fetch_post()
#         if post:
#             print("📝", post["title"])
#             print("📄", post["body"][:100], "...\n")
#             for i, c in enumerate(post["comments"][:5], 1):
#                 print(f"{i}. {c['author']} ({c['score']} pts): {c['body'][:120]}")
