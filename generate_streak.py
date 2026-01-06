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
            createdAt
        }
    }
    """
    
    # Try to use GitHub token if available
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
            calendar = data['data']['user']['contributionsCollection']['contributionCalendar']
            created_at = data['data']['user']['createdAt']
            return calendar, created_at
    except Exception as e:
        print(f"GraphQL API error: {e}")
    
    return None, None

def calculate_streaks(calendar):
    """Calculate current and longest streaks from contribution calendar"""
    if not calendar:
        return 0, 0, "N/A", "N/A", "N/A", 0
    
    # Flatten all contribution days
    all_days = []
    for week in calendar['weeks']:
        for day in week['contributionDays']:
            all_days.append({
                'date': day['date'],
                'count': day['contributionCount']
            })
    
    # Sort by date
    all_days.sort(key=lambda x: x['date'])
    
    total_contributions = calendar['totalContributions']
    
    # Calculate streaks
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    
    longest_start = None
    longest_end = None
    current_start = None
    current_end = None
    temp_start = None
    
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    for i, day in enumerate(all_days):
        if day['count'] > 0:
            if temp_streak == 0:
                temp_start = day['date']
            temp_streak += 1
            
            if temp_streak > longest_streak:
                longest_streak = temp_streak
                longest_start = temp_start
                longest_end = day['date']
        else:
            temp_streak = 0
            temp_start = None
    
    # Calculate current streak (must include today or yesterday)
    for day in reversed(all_days):
        if day['date'] == today or day['date'] == yesterday:
            if day['count'] > 0 or (day['date'] == today):
                # Count backwards from today/yesterday
                for d in reversed(all_days):
                    if d['count'] > 0:
                        current_streak += 1
                        if current_end is None:
                            current_end = d['date']
                        current_start = d['date']
                    else:
                        if current_streak > 0:
                            break
                break
        elif day['count'] == 0 and day['date'] < yesterday:
            break
    
    # Format dates
    def format_date(date_str):
        if not date_str:
            return "N/A"
        try:
            dt = datetime.strptime(date_str, '%Y-%m-%d')
            return dt.strftime('%b %d')
        except:
            return date_str
    
    # Get first contribution date
    first_date = all_days[0]['date'] if all_days else "N/A"
    
    current_range = f"{format_date(current_start)} - {format_date(current_end)}" if current_start else "N/A"
    longest_range = f"{format_date(longest_start)} - {format_date(longest_end)}" if longest_start else "N/A"
    
    return current_streak, longest_streak, current_range, longest_range, first_date, total_contributions

def generate_streak_svg():
    """Generate the streak stats SVG"""
    calendar, created_at = fetch_contribution_data()
    current_streak, longest_streak, current_range, longest_range, first_date, total = calculate_streaks(calendar)
    
    # Parse first contribution date for display
    try:
        first_dt = datetime.strptime(first_date, '%Y-%m-%d')
        first_display = first_dt.strftime('%b %d, %Y')
    except:
        first_display = first_date
    
    svg = f'''<svg width="495" height="195" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#0a0a0a"/>
            <stop offset="100%" style="stop-color:#1a1a1a"/>
        </linearGradient>
        <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" style="stop-color:#ffffff"/>
            <stop offset="100%" style="stop-color:#606060"/>
        </linearGradient>
    </defs>
    
    <style>
        .title {{ font-family: 'Segoe UI', sans-serif; font-size: 12px; fill: #808080; }}
        .value {{ font-family: 'Segoe UI', sans-serif; font-size: 28px; font-weight: bold; fill: #ffffff; }}
        .value-large {{ font-family: 'Segoe UI', sans-serif; font-size: 42px; font-weight: bold; fill: #ffffff; }}
        .label {{ font-family: 'Segoe UI', sans-serif; font-size: 10px; fill: #606060; }}
        .ring {{ fill: none; stroke-width: 5; }}
        .divider {{ stroke: #2a2a2a; stroke-width: 1; }}
    </style>
    
    <!-- Background -->
    <rect width="495" height="195" fill="url(#bgGrad)" rx="10"/>
    <rect width="495" height="3" fill="url(#accentGrad)" rx="10"/>
    
    <!-- Dividers -->
    <line x1="165" y1="30" x2="165" y2="165" class="divider"/>
    <line x1="330" y1="30" x2="330" y2="165" class="divider"/>
    
    <!-- Total Contributions (Left) -->
    <g transform="translate(82.5, 97)">
        <text class="value" text-anchor="middle" y="0">{total}</text>
        <text class="title" text-anchor="middle" y="25">Total Contributions</text>
        <text class="label" text-anchor="middle" y="42">{first_display} - Present</text>
    </g>
    
    <!-- Current Streak (Center - with Ring) -->
    <g transform="translate(247.5, 97)">
        <!-- Outer ring background -->
        <circle cx="0" cy="-10" r="38" class="ring" stroke="#1a1a1a"/>
        <!-- Animated ring -->
        <circle cx="0" cy="-10" r="38" class="ring" stroke="#ffffff" stroke-dasharray="238.76" stroke-dashoffset="{238.76 - (min(current_streak, 30) / 30 * 238.76)}" stroke-linecap="round" transform="rotate(-90 0 -10)">
            <animate attributeName="stroke-dashoffset" from="238.76" to="{238.76 - (min(current_streak, 30) / 30 * 238.76)}" dur="1.5s" fill="freeze"/>
        </circle>
        <!-- Value inside ring -->
        <text class="value-large" text-anchor="middle" y="5">{current_streak}</text>
        <text class="title" text-anchor="middle" y="50">Current Streak</text>
        <text class="label" text-anchor="middle" y="65">{current_range}</text>
    </g>
    
    <!-- Longest Streak (Right) -->
    <g transform="translate(412.5, 97)">
        <text class="value" text-anchor="middle" y="0">{longest_streak}</text>
        <text class="title" text-anchor="middle" y="25">Longest Streak</text>
        <text class="label" text-anchor="middle" y="42">{longest_range}</text>
    </g>
</svg>'''
    
    with open('streak.svg', 'w') as f:
        f.write(svg)
    
    print("Streak SVG generated!")

if __name__ == "__main__":
    generate_streak_svg()
