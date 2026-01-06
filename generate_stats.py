import requests
import json

USERNAME = "MeghVyas3132"
API_BASE = "https://api.github.com"

def fetch_github_stats():
    try:
        # Fetch user data
        user_response = requests.get(f"{API_BASE}/users/{USERNAME}")
        user_response.raise_for_status()  # Raise exception for bad status codes
        user_data = user_response.json()
        
        # Fetch repositories
        repos_response = requests.get(f"{API_BASE}/users/{USERNAME}/repos?per_page=100")
        repos_response.raise_for_status()
        repos_data = repos_response.json()
        
        # Check if we got valid data (not rate limit error)
        if isinstance(repos_data, dict) and 'message' in repos_data:
            raise Exception(f"API Error: {repos_data['message']}")
        
        # Calculate stats
        total_stars = sum(repo['stargazers_count'] for repo in repos_data)
        total_forks = sum(repo['forks_count'] for repo in repos_data)
    except Exception as e:
        print(f"⚠️ API Error: {e}. Using fallback values.")
        # Fallback values when API fails
        user_data = {'public_repos': 15, 'followers': 50}
        repos_data = []
        total_stars = 25
        total_forks = 10
    
    # Calculate languages
    languages = {}
    for repo in repos_data:
        if isinstance(repo, dict) and repo.get('language'):
            languages[repo['language']] = languages.get(repo['language'], 0) + 1
    
    # Sort languages (handle empty case)
    sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5] if languages else []
    total_lang_repos = sum(count for _, count in sorted_languages) if sorted_languages else 1
    
    # Language colors (monochrome)
    colors = {
        'JavaScript': '#e0e0e0',
        'Python': '#b0b0b0',
        'TypeScript': '#c8c8c8',
        'Go': '#909090',
        'Java': '#d0d0d0',
        'HTML': '#a0a0a0',
        'CSS': '#c0c0c0',
        'Shell': '#b8b8b8',
        'C': '#888888',
        'C++': '#989898'
    }
    
    # Generate language bars
    lang_bars = ""
    for idx, (lang, count) in enumerate(sorted_languages):
        percentage = (count / total_lang_repos * 100) if total_lang_repos > 0 else 0
        y_pos = 65 + (idx * 25)
        color = colors.get(lang, '#ff6b6b')
        
        lang_bars += f'''
        <circle cx="260" cy="{y_pos - 5}" r="5" fill="{color}"/>
        <text x="275" y="{y_pos}" font-family="Segoe UI, sans-serif" font-size="12" fill="#fff">
            {lang}
        </text>
        <text x="460" y="{y_pos}" font-family="Segoe UI, sans-serif" font-size="12" fill="#aaa" text-anchor="end">
            {percentage:.1f}%
        </text>
        '''
    
    # Generate SVG
    svg = f'''<svg width="495" height="195" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#0a0a0a;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#1a1a1a;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#ffffff;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#808080;stop-opacity:1" />
        </linearGradient>
    </defs>
    
    <rect width="495" height="195" fill="url(#grad1)" rx="10"/>
    <rect width="495" height="3" fill="url(#grad2)" rx="10"/>
    
    <text x="20" y="35" font-family="Segoe UI, sans-serif" font-size="20" font-weight="bold" fill="#ffffff">
        GitHub Stats
    </text>
    
    <text x="20" y="65" font-family="Segoe UI, sans-serif" font-size="14" fill="#808080">Total Stars:</text>
    <text x="140" y="65" font-family="Segoe UI, sans-serif" font-size="14" font-weight="bold" fill="#fff">{total_stars}</text>
    
    <text x="20" y="90" font-family="Segoe UI, sans-serif" font-size="14" fill="#808080">Public Repos:</text>
    <text x="140" y="90" font-family="Segoe UI, sans-serif" font-size="14" font-weight="bold" fill="#fff">{user_data['public_repos']}</text>
    
    <text x="20" y="115" font-family="Segoe UI, sans-serif" font-size="14" fill="#808080">Total Forks:</text>
    <text x="140" y="115" font-family="Segoe UI, sans-serif" font-size="14" font-weight="bold" fill="#fff">{total_forks}</text>
    
    <text x="20" y="140" font-family="Segoe UI, sans-serif" font-size="14" fill="#808080">Followers:</text>
    <text x="140" y="140" font-family="Segoe UI, sans-serif" font-size="14" font-weight="bold" fill="#fff">{user_data['followers']}</text>
    
    <text x="250" y="35" font-family="Segoe UI, sans-serif" font-size="16" font-weight="bold" fill="#ffffff">
        Top Languages
    </text>
    
    {lang_bars}
</svg>'''
    
    # Save SVG
    with open('stats.svg', 'w') as f:
        f.write(svg)
    
    print("Stats SVG generated successfully!")

if __name__ == "__main__":
    fetch_github_stats()
