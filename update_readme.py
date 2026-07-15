import urllib.request
import json
import re
import os
import subprocess
from datetime import datetime

def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def update_readme():
    try:
        username = "ecclesyia"
        
        # Resolve paths dynamically
        if os.environ.get("GITHUB_ACTIONS"):
            base_dir = "."
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
        config_path = os.path.join(base_dir, "profile.config.json")
        readme_path = os.path.join(base_dir, "README.md")
        
        # 1. Fetch live repository count
        print("Fetching live repository count from GitHub...")
        user_data = fetch_json(f"https://api.github.com/users/{username}")
        total_public_repos = user_data.get("public_repos", 0)
        
        # 2. Update profile.config.json
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            
        config["profile"]["totalRepos"] = total_public_repos
        
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2)
        print(f"Updated profile.config.json with totalRepos = {total_public_repos}")
        
        # 3. Fetch all repositories to calculate yearly breakdown
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
            
        by_year = {}
        for r in repos:
            c_at = r.get("created_at")
            if c_at:
                dt = datetime.strptime(c_at, "%Y-%m-%dT%H:%M:%SZ")
                year = dt.year
                by_year[year] = by_year.get(year, 0) + 1
                
        # 4. Run node generation script to rebuild SVGs and README
        print("Rebuilding SVG console assets and base README via Node...")
        cmd = ["npm", "run", "generate", "--", "--source", "portrait.png"]
        subprocess.run(cmd, cwd=base_dir, shell=True, check=True)
        
        # 5. Inject/Replace Yearly Repository History at the bottom of README
        history_section = "\n## Repository History\n\nThe table below shows the distribution of public repositories created per year:\n\n"
        history_section += "| Year | Repositories Created |\n"
        history_section += "| :--- | :--- |\n"
        for y in sorted(by_year.keys(), reverse=True):
            history_section += f"| {y} | {by_year[y]} |\n"
            
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
            
        if "## Repository History" in readme_content:
            # Replace old history section
            pattern = r"## Repository History.*"
            updated_content = re.sub(pattern, history_section.strip(), readme_content, flags=re.DOTALL)
        else:
            # Find the footer and insert before it, or append at the end
            parts = readme_content.rsplit("---", 1)
            if len(parts) == 2:
                updated_content = parts[0] + "---\n" + history_section + "\n---\n" + parts[1]
            else:
                updated_content = readme_content.strip() + "\n" + history_section
                
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("Repository history successfully appended/updated in README.md.")
        
    except Exception as e:
        print(f"Error during update process: {e}")

if __name__ == "__main__":
    update_readme()
