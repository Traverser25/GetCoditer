from db_operation import SQLiteHandler
def print_candidates(candidates, title="Results"):
    print(f"\n🔎 {title} ({len(candidates)} found)")
    for i, c in enumerate(candidates, 1):
        print(f"{i}. {c['author']} | {c['location']} | {c['experience_years']} yrs")
        print(f"   🔧 Stack: {', '.join(c['tech_stack']) or 'N/A'}")
        if c['cv_link']:
            print(f"   📄 CV: {c['cv_link']}")

def run_tests():
    db = SQLiteHandler("candidates.db")

    # 1. All candidates
    all_data = db.get_all()
    print_candidates(all_data, "All Candidates")

    # 2. Filter by Tech Stack (Python AND Node.js)
    filtered_tech = db.filter_candidates(techs=["Python", "Node.js"])
    print_candidates(filtered_tech, "Python + Node.js Candidates")

    # 3. Filter by Location (any match from list)
    loc_filtered = db.filter_candidates(locations=["Bengaluru", "Remote"])
    print_candidates(loc_filtered, "Location: Bengaluru OR Remote")

    # 4. Filter by Minimum YOE
    experienced = db.filter_candidates(min_yoe=2.0)
    print_candidates(experienced, "Experience ≥ 2 years")

    # 5. Combined filters
    combined = db.filter_candidates(techs=["AWS", "Docker"], locations=["Remote"], min_yoe=3.0)
    print_candidates(combined, "AWS+Docker | Remote | ≥3 YOE")

 

    db.close()

if __name__ == "__main__":
    run_tests()