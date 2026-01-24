import requests

USERNAME = "MeghVyas3132"
API_BASE = "https://api.github.com"

def fetch_github_data():
    """Fetch user data for trophy calculation"""
    try:
        # Fetch user data
        user_response = requests.get(f"{API_BASE}/users/{USERNAME}")
        user_data = user_response.json()
        
        # Fetch repositories
        repos_response = requests.get(f"{API_BASE}/users/{USERNAME}/repos?per_page=100")
        repos_data = repos_response.json()
        
        if isinstance(repos_data, dict) and 'message' in repos_data:
            raise Exception(repos_data['message'])
        
        # Calculate stats
        total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)
        total_forks = sum(repo.get('forks_count', 0) for repo in repos_data)
        total_repos = len(repos_data)
        followers = user_data.get('followers', 0)
        following = user_data.get('following', 0)
        
        # Count commits (approximate from repos)
        total_commits = 0
        for repo in repos_data[:10]:  # Limit to avoid rate limits
            try:
                commits_response = requests.get(f"{API_BASE}/repos/{USERNAME}/{repo['name']}/commits?per_page=1")
                if 'Link' in commits_response.headers:
                    # Parse the last page number from Link header
                    link = commits_response.headers['Link']
                    if 'last' in link:
                        import re
                        match = re.search(r'page=(\d+)>; rel="last"', link)
                        if match:
                            total_commits += int(match.group(1))
                else:
                    total_commits += len(commits_response.json()) if isinstance(commits_response.json(), list) else 0
            except:
                pass
        
        # Count issues and PRs
        issues_count = 0
        prs_count = 0
        
        return {
            'stars': total_stars,
            'forks': total_forks,
            'repos': total_repos,
            'followers': followers,
            'following': following,
            'commits': total_commits,
            'issues': issues_count,
            'prs': prs_count
        }
    except Exception as e:
        print(f"API Error: {e}")
        return {
            'stars': 25, 'forks': 10, 'repos': 15, 'followers': 50,
            'following': 30, 'commits': 500, 'issues': 20, 'prs': 15
        }

def get_trophy_rank(value, thresholds):
    """Get trophy rank based on value and thresholds"""
    ranks = ['S', 'AAA', 'AA', 'A', 'B', 'C', 'none']
    for i, threshold in enumerate(thresholds):
        if value >= threshold:
            return ranks[i]
    return 'none'

def generate_trophy(x, y, title, rank, icon):
    """Generate a single trophy SVG element"""
    # Rank colors (monochrome with subtle hints)
    rank_colors = {
        'S': ('#ffffff', '#e0e0e0'),
        'AAA': ('#d0d0d0', '#b0b0b0'),
        'AA': ('#b0b0b0', '#909090'),
        'A': ('#909090', '#707070'),
        'B': ('#707070', '#505050'),
        'C': ('#505050', '#404040'),
        'none': ('#303030', '#202020')
    }
    
    primary, secondary = rank_colors.get(rank, rank_colors['none'])
    
    if rank == 'none':
        opacity = "0.3"
    else:
        opacity = "1"
    
    return f'''
    <g transform="translate({x}, {y})" opacity="{opacity}">
        <!-- Trophy base -->
        <rect x="0" y="0" width="110" height="120" rx="8" fill="#0a0a0a" stroke="{secondary}" stroke-width="1"/>
        
        <!-- Trophy icon area -->
        <circle cx="55" cy="45" r="28" fill="none" stroke="{primary}" stroke-width="2"/>
        
        <!-- Icon -->
        <text x="55" y="52" text-anchor="middle" font-size="24">{icon}</text>
        
        <!-- Title -->
        <text x="55" y="90" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="11" fill="{primary}" font-weight="bold">{title}</text>
        
        <!-- Rank badge -->
        <rect x="40" y="100" width="30" height="14" rx="3" fill="{secondary}"/>
        <text x="55" y="111" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="9" fill="#0a0a0a" font-weight="bold">{rank if rank != 'none' else '-'}</text>
    </g>'''

def generate_trophies_svg():
    """Generate the trophies SVG"""
    data = fetch_github_data()
    
    # Define trophies with their thresholds
    trophies = [
        {
            'title': 'Stars',
            'icon': '⭐',
            'value': data['stars'],
            'thresholds': [100, 50, 25, 10, 5, 1]
        },
        {
            'title': 'Commits',
            'icon': '📝',
            'value': data['commits'],
            'thresholds': [1000, 500, 200, 100, 50, 10]
        },
        {
            'title': 'Followers',
            'icon': '👥',
            'value': data['followers'],
            'thresholds': [100, 50, 25, 10, 5, 1]
        },
        {
            'title': 'Repos',
            'icon': '📁',
            'value': data['repos'],
            'thresholds': [50, 30, 20, 10, 5, 1]
        },
        {
            'title': 'Forks',
            'icon': '🔱',
            'value': data['forks'],
            'thresholds': [50, 25, 10, 5, 2, 1]
        },
        {
            'title': 'Experience',
            'icon': '🏆',
            'value': data['repos'] + data['stars'] + data['followers'],
            'thresholds': [200, 100, 50, 25, 10, 5]
        }
    ]
    
    # Calculate SVG dimensions
    trophy_width = 120
    trophy_height = 130
    padding = 10
    cols = 6
    rows = 1
    
    svg_width = cols * trophy_width + padding * 2
    svg_height = rows * trophy_height + padding * 2
    
    # Generate trophy elements
    trophy_elements = ""
    for i, trophy in enumerate(trophies):
        col = i % cols
        row = i // cols
        x = padding + col * trophy_width
        y = padding + row * trophy_height
        rank = get_trophy_rank(trophy['value'], trophy['thresholds'])
        trophy_elements += generate_trophy(x, y, trophy['title'], rank, trophy['icon'])
    
    svg = f'''<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#0a0a0a"/>
            <stop offset="100%" style="stop-color:#0a0a0a"/>
        </linearGradient>
    </defs>
    
    <!-- Background (transparent) -->
    <rect width="{svg_width}" height="{svg_height}" fill="transparent"/>
    
    <!-- Trophies -->
    {trophy_elements}
</svg>'''
    
    with open('trophies.svg', 'w') as f:
        f.write(svg)
    
    print("Trophies SVG generated!")

if __name__ == "__main__":
    generate_trophies_svg()
