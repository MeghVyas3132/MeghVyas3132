import requests
import json

USERNAME = "MeghVyas3132"
API_BASE = "https://api.github.com"

def fetch_github_stats():
    # Fetch user data
    user_response = requests.get(f"{API_BASE}/users/{USERNAME}")
    user_data = user_response.json()
    
    # Fetch repositories
    repos_response = requests.get(f"{API_BASE}/users/{USERNAME}/repos?per_page=100")
    repos_data = repos_response.json()
    
    # Calculate stats
    total_stars = sum(repo['stargazers_count'] for repo in repos_data)
    total_forks = sum(repo['forks_count'] for repo in repos_data)
    
    # Calculate languages
    languages = {}
    for repo in repos_data:
        if repo['language']:
            languages[repo['language']] = languages.get(repo['language'], 0) + 1
    
    # Sort languages
    sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
    total_lang_repos = sum(count for _, count in sorted_languages)
    
    # Language colors
    colors = {
        'JavaScript': '#f7df1e',
        'Python': '#3776ab',
        'TypeScript': '#3178c6',
        'Go': '#00add8',
        'Java': '#b07219',
        'HTML': '#e34c26',
        'CSS': '#563d7c',
        'Shell': '#89e051',
        'C': '#555555',
        'C++': '#f34b7d'
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
            <stop offset="0%" style="stop-color:#1a1b27;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#2d1b69;stop-opacity:1" />
        </linearGradient>
        <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#ff6b6b;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#f06595;stop-opacity:1" />
        </linearGradient>
    </defs>
    
    <rect width="495" height="195" fill="url(#grad1)" rx="10"/>
    <rect width="495" height="3" fill="url(#grad2)" rx="10"/>
    
    <text x="20" y="35" font-family="Segoe UI, sans-serif" font-size="20" font-weight="bold" fill="#ff6b6b">
        📊 GitHub Stats
    </text>
    
    <text x="20" y="65" font-family="Segoe UI, sans-serif" font-size="14" fill="#aaa">⭐ Total Stars:</text>
    <text x="140" y="65" font-family="Segoe UI, sans-serif" font-size="14" font-weight="bold" fill="#fff">{total_stars}</text>
    
    <text x="20" y="90" font-family="Segoe UI, sans-serif" font-size="14" fill="#aaa">📦 Public Repos:</text>
    <text x="140" y="90" font-family="Segoe UI, sans-serif" font-size="14" font-weight="bold" fill="#fff">{user_data['public_repos']}</text>
    
    <text x="20" y="115" font-family="Segoe UI, sans-serif" font-size="14" fill="#aaa">🍴 Total Forks:</text>
    <text x="140" y="115" font-family="Segoe UI, sans-serif" font-size="14" font-weight="bold" fill="#fff">{total_forks}</text>
    
    <text x="20" y="140" font-family="Segoe UI, sans-serif" font-size="14" fill="#aaa">👥 Followers:</text>
    <text x="140" y="140" font-family="Segoe UI, sans-serif" font-size="14" font-weight="bold" fill="#fff">{user_data['followers']}</text>
    
    <text x="250" y="35" font-family="Segoe UI, sans-serif" font-size="16" font-weight="bold" fill="#ff6b6b">
        🔥 Top Languages
    </text>
    
    {lang_bars}
</svg>'''
    
    # Save SVG
    with open('stats.svg', 'w') as f:
        f.write(svg)
    
    print("✅ Stats SVG generated successfully!")

if __name__ == "__main__":
    fetch_github_stats()
