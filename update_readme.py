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
        
        # 5. Load generated README to inject Views Badge and monochrome widgets
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
            
        # A. Inject Views Badge right under the Terminal Console picture banner
        views_badge = """
<p align="center">
  <img src="https://komarev.com/ghpvc/?username=ecclesyia&color=000000&style=flat-square&label=Profile+Views" alt="Profile Views">
</p>
"""
        if "Profile+Views" not in readme_content:
            pattern_views = r"(</picture>\s*</p>)"
            readme_content = re.sub(pattern_views, r"\1\n" + views_badge, readme_content)
            
        # B. Generate the dynamic monochrome extra sections (History, Stats, Tech Grid, Connect)
        extra_sections = "\n## Repository History\n\nThe table below shows the distribution of public repositories created per year:\n\n"
        extra_sections += "| Year | Repositories Created |\n"
        extra_sections += "| :--- | :--- |\n"
        for y in sorted(by_year.keys(), reverse=True):
            extra_sections += f"| {y} | {by_year[y]} |\n"
            
        extra_sections += """
## GitHub Stats

<p align="center">
  <img src="https://github-readme-streak-stats.herokuapp.com/?user=ecclesyia&theme=dark&hide_border=true&background=000000&fire=ffffff&ring=ffffff&currStreakNum=ffffff&sideNums=ffffff&sideLabels=6e6e6e&currStreakLabel=ffffff" alt="GitHub Streak Stats" />
</p>

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=ecclesyia&show_icons=true&theme=dark&hide_border=true&bg_color=000000&text_color=ffffff&icon_color=ffffff&title_color=ffffff&count_private=true" alt="GitHub Stats" />
</p>

## Tools and Technologies

<p align="center">
  <img src="https://skillicons.dev/icons?i=kotlin,java,js,py,mysql,godot,html,css,react,git,androidstudio,pycharm,vscode&theme=dark" alt="My Skills" />
</p>

## Connect

<p align="center">
  <a href="https://ecclesyia.netlify.app" target="_blank">
    <img src="https://img.shields.io/badge/Portfolio-000000?style=for-the-badge&logo=netlify&logoColor=white" alt="Portfolio" />
  </a>
  <a href="mailto:ecclesiatesnsbusiness@gmail.com" target="_blank">
    <img src="https://img.shields.io/badge/Email-000000?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" />
  </a>
  <a href="https://www.linkedin.com/in/ecclesiates" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-000000?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>
  <a href="https://www.instagram.com/ecclesiates.sihombing/" target="_blank">
    <img src="https://img.shields.io/badge/Instagram-000000?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" />
  </a>
  <a href="https://x.com/ecclesyia" target="_blank">
    <img src="https://img.shields.io/badge/X-000000?style=for-the-badge&logo=x&logoColor=white" alt="X" />
  </a>
</p>
"""

        # Replace or append the dynamic extra sections
        if "## Repository History" in readme_content:
            pattern_history = r"## Repository History.*"
            updated_content = re.sub(pattern_history, extra_sections.strip(), readme_content, flags=re.DOTALL)
        else:
            parts = readme_content.rsplit("---", 1)
            if len(parts) == 2:
                updated_content = parts[0] + "---\n" + extra_sections + "\n---\n" + parts[1]
            else:
                updated_content = readme_content.strip() + "\n" + extra_sections
                
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("Dynamic monochrome sections successfully injected into README.md.")
        
    except Exception as e:
        print(f"Error during update process: {e}")

if __name__ == "__main__":
    update_readme()
