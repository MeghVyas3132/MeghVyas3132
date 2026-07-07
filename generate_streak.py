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
    
    # Risograph palette (matches portfolio megh.tech + README assets)
    PAPER, P_EDGE = "#f7e7c8", "#e6c78f"
    FLAME, INK = "#e8451c", "#16305e"
    INK_D, INK_S, INK_F = "#0d2148", "#45568a", "#8794b4"

    C = 213.63  # 2*pi*34
    frac = min(current_streak, 30) / 30.0
    offset = C * (1 - frac)

    svg = f'''<svg width="600" height="210" viewBox="0 0 600 210" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="fl" cx="92%" cy="8%" r="70%">
      <stop offset="0%" stop-color="{FLAME}" stop-opacity="0.16"/>
      <stop offset="60%" stop-color="{FLAME}" stop-opacity="0"/>
    </radialGradient>
    <radialGradient id="in" cx="4%" cy="96%" r="72%">
      <stop offset="0%" stop-color="{INK}" stop-opacity="0.12"/>
      <stop offset="64%" stop-color="{INK}" stop-opacity="0"/>
    </radialGradient>
    <filter id="gr"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch" result="n"/><feColorMatrix in="n" type="saturate" values="0"/></filter>
    <style>
      text{{font-family:'SFMono-Regular','SF Mono',Menlo,Consolas,'Liberation Mono',monospace}}
      .val{{fill:{INK_D};font-size:28px;font-weight:600}}
      .big{{fill:{FLAME};font-size:38px;font-weight:600}}
      .ttl{{fill:{INK_S};font-size:11.5px;letter-spacing:1.4px}}
      .lab{{fill:{INK_F};font-size:10px}}
    </style>
  </defs>
  <rect x="0" y="0" width="600" height="210" rx="18" fill="{PAPER}"/>
  <rect x="0" y="0" width="600" height="210" rx="18" fill="url(#fl)"/>
  <rect x="0" y="0" width="600" height="210" rx="18" fill="url(#in)"/>
  <rect x="0" y="0" width="600" height="210" rx="18" filter="url(#gr)" opacity="0.22" style="mix-blend-mode:multiply"/>
  <rect x="0.75" y="0.75" width="598.5" height="208.5" rx="17.5" fill="none" stroke="{INK}" stroke-opacity="0.14" stroke-width="1.5"/>

  <line x1="200" y1="40" x2="200" y2="170" stroke="{INK}" stroke-opacity="0.12" stroke-width="1.5"/>
  <line x1="400" y1="40" x2="400" y2="170" stroke="{INK}" stroke-opacity="0.12" stroke-width="1.5"/>

  <g transform="translate(100,104)">
    <text class="val" text-anchor="middle" y="0">{total}</text>
    <text class="ttl" text-anchor="middle" y="30">TOTAL CONTRIBUTIONS</text>
    <text class="lab" text-anchor="middle" y="48">{first_display} — Present</text>
  </g>

  <g transform="translate(300,100)">
    <circle cx="0" cy="-8" r="34" fill="none" stroke="{P_EDGE}" stroke-width="5"/>
    <circle cx="0" cy="-8" r="34" fill="none" stroke="{FLAME}" stroke-width="5" stroke-linecap="round"
            stroke-dasharray="{C:.2f}" stroke-dashoffset="{offset:.2f}" transform="rotate(-90 0 -8)"/>
    <text class="big" text-anchor="middle" y="4">{current_streak}</text>
    <text class="ttl" text-anchor="middle" y="46" fill="{INK}">CURRENT STREAK</text>
    <text class="lab" text-anchor="middle" y="63">{current_range}</text>
  </g>

  <g transform="translate(500,104)">
    <text class="val" text-anchor="middle" y="0">{longest_streak}</text>
    <text class="ttl" text-anchor="middle" y="30">LONGEST STREAK</text>
    <text class="lab" text-anchor="middle" y="48">{longest_range}</text>
  </g>
</svg>'''

    with open('streak.svg', 'w') as f:
        f.write(svg)

    print("Streak SVG generated (riso).")

if __name__ == "__main__":
    generate_streak_svg()
