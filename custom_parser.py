import re

class CommentParser:
    # --- STATIC CONFIGS ---

    FIELDS = {
        "location": ["location"],
        "relocate": ["willing to relocate", "relocate"],
        "type": ["type"],
        "notice_period": ["notice period", "np"],
        "experience": ["total years of experience", "experience", "yoe"],
        "cv_link": ["résumé/cv link", "cv", "resume"],
        "blurb": ["blurb"]
    }

    LOCATION_ALIASES = {
        "bangalore": "Bengaluru",
        "blr": "Bengaluru",
        "delhi": "Delhi",
        "hyd": "Hyderabad",
        "mumbai": "Mumbai",
        "pune": "Pune",
        "remote": "Remote"
    }

    TECH_STACK = {
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C", "Go", "Rust",
        "Django", "Flask", "FastAPI", "React", "Angular", "Vue", "Svelte", "Next.js", "Express",
        "Tailwind", "Bootstrap", "jQuery",
        "MongoDB", "PostgreSQL", "MySQL", "SQLite", "Redis", "Elasticsearch",
        "Docker", "Kubernetes", "Terraform", "Ansible", "GitHub Actions", "GitLab CI", "Jenkins",
        "Nginx", "Apache", "Heroku",
        "AWS", "GCP", "Azure", "Supabase", "Firebase", "Netlify", "Vercel", "Railway",
        "REST", "GraphQL", "gRPC", "WebSocket",
        "Power BI", "Tableau", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch",
        "Matplotlib", "Excel", "Jupyter",
        "Git", "Bitbucket", "Figma", "CI/CD", "TDD", "OAuth", "JWT", "Postman", "Linux", "Shell", "WSL",
        "DSA", "Full-Stack", "Frontend", "Backend", "Microservices", "Agile", "Scrum", "NoSQL", "SQL",
        "Responsive Design", "SEO",
        "GATE", "LeetCode", "Codeforces", "HackerRank"
    }

    def normalize_experience(self, raw: str) -> float:
        raw = raw.strip().lower()
        if "fresher" in raw:
            return 0.0
        match = re.search(r"(\d+(\.\d+)?)\+?\s*(year|yr)", raw)
        return float(match.group(1)) if match else 0.0

    def normalize_location(self, raw: str) -> str:
        raw = raw.lower().strip()
        for alias, standard in self.LOCATION_ALIASES.items():
            if alias in raw:
                return standard
        return raw.title()

    def extract_fields(self, comment_text: str) -> dict:
        result = {key: "" for key in self.FIELDS}
        blurb_lines = []

        lines = comment_text.splitlines()

        for line in lines:
            line = line.strip()
            matched = False
            for key in list(self.FIELDS.keys())[:-1]:  # exclude 'blurb'
                for label in self.FIELDS[key]:
                    if line.lower().startswith(label + ":"):
                        result[key] = line.split(":", 1)[1].strip()
                        matched = True
                        break
                if matched:
                    break
            if not matched:
                blurb_lines.append(line)

        if not result["blurb"]:
            result["blurb"] = "\n".join(blurb_lines).strip()

        result["experience_years"] = self.normalize_experience(result["experience"])
        result["location"] = self.normalize_location(result["location"])

        cv = result.get("cv_link", "").strip().lower()
        result["cv_is_link"] = cv.startswith("http://") or cv.startswith("https://")

        return result

    def detect_tech_stack(self, text: str) -> list:
        found = []
        for tech in self.TECH_STACK:
            if tech.lower() in text.lower():
                found.append(tech)
        return sorted(set(found))

    def serialize(self, comment: dict) -> dict:
        fields = self.extract_fields(comment.get("body", ""))
        techs = self.detect_tech_stack(fields.get("blurb", ""))
        return {
            "author": comment.get("author", "[unknown]"),
            "score": comment.get("score", 0),
            **fields,
            "tech_stack": techs
        }
import re

class CommentParser:
    # --- STATIC CONFIGS ---

    FIELDS = {
        "location": ["location"],
        "relocate": ["willing to relocate", "relocate"],
        "type": ["type"],
        "notice_period": ["notice period", "np"],
        "experience": ["total years of experience", "experience", "yoe"],
        "cv_link": ["résumé/cv link", "cv", "resume"],
        "blurb": ["blurb"]
    }

    LOCATION_ALIASES = {
        "bangalore": "Bengaluru",
        "blr": "Bengaluru",
        "delhi": "Delhi",
        "hyd": "Hyderabad",
        "mumbai": "Mumbai",
        "pune": "Pune",
        "remote": "Remote"
    }

    TECH_STACK = {
        "Python", "JavaScript", "TypeScript", "Java", "C++", "C", "Go", "Rust",
        "Django", "Flask", "FastAPI", "React", "Angular", "Vue", "Svelte", "Next.js", "Express",
        "Tailwind", "Bootstrap", "jQuery",
        "MongoDB", "PostgreSQL", "MySQL", "SQLite", "Redis", "Elasticsearch",
        "Docker", "Kubernetes", "Terraform", "Ansible", "GitHub Actions", "GitLab CI", "Jenkins",
        "Nginx", "Apache", "Heroku",
        "AWS", "GCP", "Azure", "Supabase", "Firebase", "Netlify", "Vercel", "Railway",
        "REST", "GraphQL", "gRPC", "WebSocket",
        "Power BI", "Tableau", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "PyTorch",
        "Matplotlib", "Excel", "Jupyter",
        "Git", "Bitbucket", "Figma", "CI/CD", "TDD", "OAuth", "JWT", "Postman", "Linux", "Shell", "WSL",
        "DSA", "Full-Stack", "Frontend", "Backend", "Microservices", "Agile", "Scrum", "NoSQL", "SQL",
        "Responsive Design", "SEO",
        "GATE", "LeetCode", "Codeforces", "HackerRank"
    }

    def normalize_experience(self, raw: str) -> float:
        raw = raw.strip().lower()
        if "fresher" in raw:
            return 0.0
        match = re.search(r"(\d+(\.\d+)?)\+?\s*(year|yr)", raw)
        return float(match.group(1)) if match else 0.0

    def normalize_location(self, raw: str) -> str:
        raw = raw.lower().strip()
        for alias, standard in self.LOCATION_ALIASES.items():
            if alias in raw:
                return standard
        return raw.title()

    def extract_fields(self, comment_text: str) -> dict:
        result = {key: "" for key in self.FIELDS}
        blurb_lines = []

        lines = comment_text.splitlines()

        for line in lines:
            line = line.strip()
            matched = False
            for key in list(self.FIELDS.keys())[:-1]:  # exclude 'blurb'
                for label in self.FIELDS[key]:
                    if line.lower().startswith(label + ":"):
                        result[key] = line.split(":", 1)[1].strip()
                        matched = True
                        break
                if matched:
                    break
            if not matched:
                blurb_lines.append(line)

        if not result["blurb"]:
            result["blurb"] = "\n".join(blurb_lines).strip()

        result["experience_years"] = self.normalize_experience(result["experience"])
        result["location"] = self.normalize_location(result["location"])

        cv = result.get("cv_link", "").strip().lower()
        result["cv_is_link"] = cv.startswith("http://") or cv.startswith("https://")

        return result

    def detect_tech_stack(self, text: str) -> list:
        found = []
        for tech in self.TECH_STACK:
            if tech.lower() in text.lower():
                found.append(tech)
        return sorted(set(found))

    def serialize(self, comment: dict) -> dict:
        fields = self.extract_fields(comment.get("body", ""))
        techs = self.detect_tech_stack(fields.get("blurb", ""))
        return {
            "author": comment.get("author", "[unknown]"),
            "score": comment.get("score", 0),
            **fields,
            "tech_stack": techs
        }
