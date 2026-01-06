import requests
from datetime import datetime, timedelta

USERNAME = "MeghVyas3132"

def fetch_contribution_data():
    """Fetch contribution data from GitHub GraphQL API"""
    query = """
    query($username: String!) {
        user(login: $username) {
            contributionsCollection {
                contributionCalendar {
                    totalContributions
                    weeks {
                        contributionDays {
                            contributionCount
                            date
                        }
                    }
                }
            }
        }
    }
    """
    
    import os
    token = os.environ.get('GITHUB_TOKEN', '')
    
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        response = requests.post(
            'https://api.github.com/graphql',
            json={'query': query, 'variables': {'username': USERNAME}},
            headers=headers
        )
        data = response.json()
        
        if 'data' in data and data['data']['user']:
            return data['data']['user']['contributionsCollection']['contributionCalendar']
    except Exception as e:
        print(f"GraphQL API error: {e}")
    
    return None

def generate_contribution_graph():
    """Generate contribution graph SVG"""
    calendar = fetch_contribution_data()
    
    # Get last 30 days of contributions
    contributions = []
    if calendar:
        all_days = []
        for week in calendar['weeks']:
            for day in week['contributionDays']:
                all_days.append({
                    'date': day['date'],
                    'count': day['contributionCount']
                })
        # Get last 30 days
        contributions = all_days[-30:] if len(all_days) >= 30 else all_days
    else:
        # Fallback data
        today = datetime.now()
        for i in range(30):
            date = today - timedelta(days=29-i)
            contributions.append({
                'date': date.strftime('%Y-%m-%d'),
                'count': (i * 3) % 15
            })
    
    # Calculate max for scaling
    max_count = max(d['count'] for d in contributions) if contributions else 1
    if max_count == 0:
        max_count = 1
    
    # SVG dimensions
    width = 900
    height = 320
    padding_left = 60
    padding_right = 30
    padding_top = 60
    padding_bottom = 60
    graph_width = width - padding_left - padding_right
    graph_height = height - padding_top - padding_bottom
    
    # Generate path for the line
    points = []
    for i, day in enumerate(contributions):
        x = padding_left + (i / (len(contributions) - 1)) * graph_width if len(contributions) > 1 else padding_left
        y = padding_top + graph_height - (day['count'] / max_count * graph_height)
        points.append((x, y))
    
    # Create smooth path
    path_d = f"M {points[0][0]},{points[0][1]}"
    for i in range(1, len(points)):
        path_d += f" L {points[i][0]},{points[i][1]}"
    
    # Area path (for gradient fill)
    area_d = path_d + f" L {points[-1][0]},{padding_top + graph_height} L {points[0][0]},{padding_top + graph_height} Z"
    
    # Generate dots and labels
    dots_svg = ""
    labels_svg = ""
    for i, (point, day) in enumerate(zip(points, contributions)):
        # Dots
        dots_svg += f'<circle cx="{point[0]}" cy="{point[1]}" r="4" fill="#ffffff" stroke="#0a0a0a" stroke-width="2"/>\n'
        
        # X-axis labels (every 3rd day)
        if i % 3 == 0 or i == len(contributions) - 1:
            try:
                dt = datetime.strptime(day['date'], '%Y-%m-%d')
                label = dt.strftime('%d')
            except:
                label = str(i)
            labels_svg += f'<text x="{point[0]}" y="{height - 25}" text-anchor="middle" font-size="11" fill="#606060">{label}</text>\n'
    
    # Y-axis labels
    y_labels_svg = ""
    steps = 5
    for i in range(steps + 1):
        y_val = int(max_count * (steps - i) / steps)
        y_pos = padding_top + (i / steps) * graph_height
        y_labels_svg += f'<text x="{padding_left - 15}" y="{y_pos + 4}" text-anchor="end" font-size="11" fill="#606060">{y_val}</text>\n'
        y_labels_svg += f'<line x1="{padding_left}" y1="{y_pos}" x2="{width - padding_right}" y2="{y_pos}" stroke="#1a1a1a" stroke-width="1"/>\n'
    
    svg = f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#0a0a0a"/>
            <stop offset="100%" style="stop-color:#1a1a1a"/>
        </linearGradient>
        <linearGradient id="lineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#808080"/>
            <stop offset="100%" style="stop-color:#ffffff"/>
        </linearGradient>
        <linearGradient id="areaGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" style="stop-color:#ffffff;stop-opacity:0.15"/>
            <stop offset="100%" style="stop-color:#ffffff;stop-opacity:0"/>
        </linearGradient>
    </defs>
    
    <!-- Background -->
    <rect width="{width}" height="{height}" fill="url(#bgGrad)" rx="10"/>
    
    <!-- Title -->
    <text x="{width/2}" y="35" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="18" font-weight="bold" fill="#ffffff">Contribution Graph</text>
    
    <!-- Grid lines -->
    {y_labels_svg}
    
    <!-- Y-axis label -->
    <text x="20" y="{height/2}" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="12" fill="#808080" transform="rotate(-90, 20, {height/2})">Contributions</text>
    
    <!-- X-axis label -->
    <text x="{width/2}" y="{height - 8}" text-anchor="middle" font-family="'Segoe UI', sans-serif" font-size="12" fill="#808080">Days</text>
    
    <!-- Area fill -->
    <path d="{area_d}" fill="url(#areaGrad)"/>
    
    <!-- Line -->
    <path d="{path_d}" fill="none" stroke="url(#lineGrad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <animate attributeName="stroke-dashoffset" from="2000" to="0" dur="2s" fill="freeze"/>
    </path>
    
    <!-- Dots -->
    {dots_svg}
    
    <!-- X-axis labels -->
    {labels_svg}
</svg>'''
    
    with open('contribution-graph.svg', 'w') as f:
        f.write(svg)
    
    print("Contribution graph generated!")

if __name__ == "__main__":
    generate_contribution_graph()
