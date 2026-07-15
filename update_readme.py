import urllib.request
import json
import re
from datetime import datetime

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def get_stats():
    username = "ecclesyia"
    start_year = 2023
    start_month = 1 # January

    # Calculate coding duration
    now = datetime.utcnow()
    years = now.year - start_year
    months = now.month - start_month
    if months < 0:
        years -= 1
        months += 12

    duration_str = f"{years} Years, {months} Months" if months > 0 else f"{years} Years"

    # Fetch user details
    user_data = fetch_json(f"https://api.github.com/users/{username}")
    total_public_repos = user_data.get("public_repos", 0)

    # Fetch all repositories (supporting pagination)
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/repos?per_page=100&page={page}"
        page_repos = fetch_json(url)
        if not page_repos:
            break
        repos.extend(page_repos)
        if len(page_repos) < 100:
            break
        page += 1

    # Count repositories by year
    by_year = {}
    for r in repos:
        c_at = r.get("created_at")
        if c_at:
            dt = datetime.strptime(c_at, "%Y-%m-%dT%H:%M:%SZ")
            year = dt.year
            by_year[year] = by_year.get(year, 0) + 1

    # Generate Markdown content for dynamic stats
    stats_md = []
    stats_md.append(f"* **Coding Experience**: Since January 2023 ({duration_str})")
    stats_md.append(f"* **Total Public Repositories**: {total_public_repos}")
    stats_md.append("")
    stats_md.append("### Repositories Created per Year")
    stats_md.append("")
    stats_md.append("| Year | Repositories Created |")
    stats_md.append("| :--- | :--- |")
    for y in sorted(by_year.keys(), reverse=True):
        stats_md.append(f"| {y} | {by_year[y]} |")
    
    return "\n".join(stats_md)

def update_readme():
    try:
        stats_content = get_stats()
        
        # Resolve path dynamically for local testing and GitHub Actions
        import os
        if os.environ.get("GITHUB_ACTIONS"):
            readme_path = "README.md"
        else:
            readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
        
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Locate tags and replace everything between them
        pattern = r"(<!-- START_SECTION:dynamic_stats -->).*?(<!-- END_SECTION:dynamic_stats -->)"
        replacement = f"\\1\n{stats_content}\n\\2"
        
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
            
        print("README.md updated successfully with dynamic stats.")
        
    except Exception as e:
        print(f"Error updating README: {e}")

if __name__ == "__main__":
    update_readme()
