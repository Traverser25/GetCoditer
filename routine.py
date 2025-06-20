from reddit_scrapper import RedditScraper
from custom_parser import CommentParser
from db_operation import SQLiteHandler  

# --- CONFIG ---
DB_PATH = "candidates.db"
PERMALINK = "/r/developersIndia/comments/1l0gai1/whos_looking_for_work_monthly_megathread_june_2025/"

def main():
    print("🔍 Fetching Reddit post...")
    scraper = RedditScraper()
    post = scraper.fetch_post(PERMALINK)

    if not post:
        print("❌ Could not retrieve Reddit post.")
        return

    print(f"📝 Post Title: {post['title']}")
    print(f"💬 Total Comments: {len(post['comments'])}\n")

    parser = CommentParser()
    db = SQLiteHandler(DB_PATH)
    inserted_count = 0

    for comment in post["comments"]:
        try:
            data = parser.serialize(comment)
            if not data.get("blurb") or not data.get("tech_stack"):
                continue  # skip poor data

            db.insert_candidate(data)
            inserted_count += 1

        except Exception as e:
            print(f"⚠️ Skipped one comment due to error: {e}")
        if(inserted_count>=5):
            pass
    db.close()
    print(f"\n✅ Done. Inserted {inserted_count} structured candidates into '{DB_PATH}'.")

if __name__ == "__main__":
    main()
