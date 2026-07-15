import urllib.request
import json
import re
import os
import io
from datetime import datetime
from PIL import Image

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

    # Generate Markdown content for dynamic stats (only the year table)
    stats_md = []
    stats_md.append("| Year | Repositories Created |")
    stats_md.append("| :--- | :--- |")
    for y in sorted(by_year.keys(), reverse=True):
        stats_md.append(f"| {y} | {by_year[y]} |")
    
    stats_content = "\n".join(stats_md)
    
    return stats_content, duration_str, total_public_repos

def get_ascii_portrait():
    # Attempt to load local portrait, fallback to GitHub avatar
    img = None
    local_path = "portrait.png"
    if os.path.exists(local_path):
        try:
            img = Image.open(local_path)
            print("Loaded local portrait.png for ASCII conversion.")
        except Exception as e:
            print(f"Error loading local portrait.png: {e}")
            
    if img is None:
        try:
            avatar_url = "https://avatars.githubusercontent.com/u/120638975?v=4"
            print("Fetching GitHub avatar for ASCII conversion...")
            req = urllib.request.Request(avatar_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as resp:
                img_data = resp.read()
            img = Image.open(io.BytesIO(img_data))
        except Exception as e:
            print(f"Error fetching GitHub avatar: {e}")
            return None

    # Calculate height based on monospace font aspect ratio (0.55 multiplier)
    width = 36
    height = int(width * (img.height / img.width) * 0.55)
    
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    img = img.convert("RGBA")
    
    chars = " .:-=+*#%@"
    ascii_lines = []
    for y in range(height):
        line = ""
        for x in range(width):
            r, g, b, a = img.getpixel((x, y))
            if a < 50:
                line += " "
            else:
                gray = int(0.299 * r + 0.587 * g + 0.114 * b)
                idx = int((gray / 255) * (len(chars) - 1))
                line += chars[idx]
        ascii_lines.append(line)
        
    return ascii_lines

def generate_svg(duration_str, total_repos, output_dir):
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get ASCII portrait
    ascii_lines = get_ascii_portrait()
    
    # Fallback to stylized logo if ASCII generation failed
    if not ascii_lines:
        ascii_lines = [
            "  ███████╗  ",
            "  ██╔════╝  ",
            "  ███████╗  ",
            "  ██╔════╝  ",
            "  ███████╗  ",
            "  ╚══════╝  "
        ]
        ascii_y_start = 150
        ascii_font_size = 14
        ascii_line_height = 20
        ascii_color_class = "accent"
    else:
        ascii_y_start = 100
        ascii_font_size = 9
        ascii_line_height = 12
        ascii_color_class = "portrait-color"
    
    # Generate SVG XML for the ASCII lines
    ascii_elements = []
    for i, line in enumerate(ascii_lines):
        y_pos = ascii_y_start + (i * ascii_line_height)
        # Escape any potential XML issues (though our charset is safe)
        escaped_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        ascii_elements.append(f'<text x="30" y="{y_pos}">{escaped_line}</text>')
        
    ascii_svg_text = "\n    ".join(ascii_elements)

    svg_template = f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="360" viewBox="0 0 800 360">
  <style>
    .terminal {{ font-family: 'Fira Code', Monaco, Consolas, 'Courier New', monospace; font-weight: bold; fill: #abb2bf; }}
    .title-text {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 13px; fill: #8b949e; font-weight: 500; }}
    .prompt {{ fill: #98c379; }}
    .command {{ fill: #e5c07b; }}
    .accent {{ fill: #61afef; }}
    .label {{ fill: #56b6c2; }}
    .value {{ fill: #c9d1d9; }}
    .subtle {{ fill: #5c6370; }}
    .portrait-color {{ fill: #56b6c2; font-size: {ascii_font_size}px; }}
    .cursor {{ animation: blink 1s step-end infinite; }}
    @keyframes blink {{ 50% {{ fill: transparent; }} }}
  </style>
  
  <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
    <feDropShadow dx="0" dy="8" stdDeviation="6" flood-color="#000" flood-opacity="0.5"/>
  </filter>
  <rect x="15" y="15" width="770" height="330" rx="8" ry="8" fill="#0b0f19" filter="url(#shadow)"/>
  
  <path d="M15,15 h770 a8,8 0 0 1 8,8 v22 a0,0 0 0 1 0,0 h-786 a0,0 0 0 1 0,-0 v-22 a8,8 0 0 1 8,-8 z" fill="#121620" />
  
  <circle cx="35" cy="30" r="6" fill="#ff5f56"/>
  <circle cx="55" cy="30" r="6" fill="#ffbd2e"/>
  <circle cx="75" cy="30" r="6" fill="#27c93f"/>
  
  <text x="400" y="34" text-anchor="middle" class="title-text">ecclesyia@binus: ~</text>
  
  <g class="terminal">
    <text x="30" y="75" style="font-size: 14px;"><tspan class="prompt">ecclesyia@binus:~$</tspan> <tspan class="command">neofetch</tspan></text>
    
    <!-- ASCII Art / Portrait Column -->
    <g class="{ascii_color_class}" style="font-size: {ascii_font_size}px;">
      {ascii_svg_text}
    </g>
    
    <line x1="250" y1="100" x2="250" y2="310" stroke="#1f2430" stroke-width="1"/>
    
    <g transform="translate(270, 0)" style="font-size: 13px;">
      <text x="0" y="115"><tspan class="accent">ecclesyia</tspan><tspan class="subtle">@</tspan><tspan class="prompt">binus-university</tspan></text>
      <text x="0" y="125" class="subtle">-----------------------------</text>
      
      <text x="0" y="150"><tspan class="label">OS</tspan><tspan class="subtle">: </tspan><tspan class="value">BINUS OS v2026.7</tspan></text>
      <text x="0" y="170"><tspan class="label">Host</tspan><tspan class="subtle">: </tspan><tspan class="value">HIMTI Responsi Activist</tspan></text>
      <text x="0" y="190"><tspan class="label">Kernel</tspan><tspan class="subtle">: </tspan><tspan class="value">Computer Science - Software Engineering</tspan></text>
      <text x="0" y="210"><tspan class="label">Uptime</tspan><tspan class="subtle">: </tspan><tspan class="value">{duration_str}</tspan></text>
      <text x="0" y="230"><tspan class="label">Shell</tspan><tspan class="subtle">: </tspan><tspan class="value">zsh 5.9</tspan></text>
      <text x="0" y="250"><tspan class="label">Editor</tspan><tspan class="subtle">: </tspan><tspan class="value">VS Code, Android Studio</tspan></text>
      <text x="0" y="270"><tspan class="label">Total Repos</tspan><tspan class="subtle">: </tspan><tspan class="value">{total_repos}</tspan></text>
      <text x="0" y="290"><tspan class="label">Languages</tspan><tspan class="subtle">: </tspan><tspan class="value">Kotlin, Java, JavaScript, Python, SQL, GDScript</tspan></text>
    </g>

    <text x="30" y="330" style="font-size: 14px;"><tspan class="prompt">ecclesyia@binus:~$</tspan> <rect class="cursor" x="180" y="317" width="8" height="15" fill="#58a6ff"/></text>
  </g>
</svg>"""

    svg_path = os.path.join(output_dir, "console.svg")
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_template)
    print("Terminal console SVG generated successfully.")

def update_readme():
    try:
        # Determine paths dynamically
        if os.environ.get("GITHUB_ACTIONS"):
            base_dir = "."
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            
        readme_path = os.path.join(base_dir, "README.md")
        assets_dir = os.path.join(base_dir, "assets")
        
        # Get dynamic stats
        stats_content, duration_str, total_public_repos = get_stats()
        
        # 1. Update README.md
        with open(readme_path, "r", encoding="utf-8") as f:
            content = f.read()

        pattern = r"(<!-- START_SECTION:dynamic_stats -->).*?(<!-- END_SECTION:dynamic_stats -->)"
        replacement = f"\\1\n{stats_content}\n\\2"
        updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print("README.md updated successfully with dynamic stats.")
        
        # 2. Generate updated console SVG
        generate_svg(duration_str, total_public_repos, assets_dir)
        
    except Exception as e:
        print(f"Error updating README and SVG: {e}")

if __name__ == "__main__":
    update_readme()
