import requests

USERNAME = "MeghVyas3132"
API_BASE = "https://api.github.com"

# ---- Risograph palette (matches portfolio megh.tech + README assets) --------
PAPER   = "#f7e7c8"
P_EDGE  = "#e6c78f"
FLAME   = "#e8451c"
INK     = "#16305e"
INK_D   = "#0d2148"
INK_S   = "#45568a"
INK_F   = "#8794b4"
LANG_COLORS = ["#e8451c", "#16305e", "#c8390f", "#45568a", "#f5411a"]


def fetch_github_stats():
    try:
        user_data = requests.get(f"{API_BASE}/users/{USERNAME}").json()
        repos_data = requests.get(f"{API_BASE}/users/{USERNAME}/repos?per_page=100").json()
        if isinstance(repos_data, dict) and "message" in repos_data:
            raise Exception(repos_data["message"])
        total_stars = sum(r["stargazers_count"] for r in repos_data)
        total_forks = sum(r["forks_count"] for r in repos_data)
    except Exception as e:
        print(f"API Error: {e}. Using fallback values.")
        user_data = {"public_repos": 32, "followers": 37}
        repos_data = []
        total_stars, total_forks = 35, 2

    languages = {}
    for repo in repos_data:
        if isinstance(repo, dict) and repo.get("language"):
            languages[repo["language"]] = languages.get(repo["language"], 0) + 1
    sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:5]
    total_lang = sum(c for _, c in sorted_langs) or 1
    if not sorted_langs:
        sorted_langs = [("TypeScript", 36), ("Python", 24), ("JavaScript", 20),
                        ("Go", 12), ("HTML", 8)]
        total_lang = sum(c for _, c in sorted_langs)

    # --- left column: four numbers -------------------------------------------
    stats = [("Total stars", total_stars), ("Public repos", user_data["public_repos"]),
             ("Total forks", total_forks), ("Followers", user_data["followers"])]
    left = ""
    for i, (label, val) in enumerate(stats):
        y = 84 + i * 33
        left += f'''
      <circle cx="30" cy="{y-6:.0f}" r="3" fill="{FLAME}"/>
      <text class="lab" x="44" y="{y}">{label}</text>
      <text class="num" x="250" y="{y}" text-anchor="end">{val}</text>'''

    # --- right column: language bars -----------------------------------------
    right = ""
    for i, (lang, count) in enumerate(sorted_langs):
        pct = count / total_lang * 100
        y = 86 + i * 26
        bw = 168 * (pct / 100.0)
        col = LANG_COLORS[i % len(LANG_COLORS)]
        right += f'''
      <text class="lang" x="320" y="{y-6:.0f}">{lang}</text>
      <text class="pct" x="560" y="{y-6:.0f}" text-anchor="end">{pct:.0f}%</text>
      <rect x="320" y="{y:.0f}" width="168" height="4" rx="2" fill="{P_EDGE}"/>
      <rect x="320" y="{y:.0f}" width="{bw:.1f}" height="4" rx="2" fill="{col}"/>'''

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
      .eb{{fill:{FLAME};font-size:13px;letter-spacing:2.4px;font-weight:600}}
      .lab{{fill:{INK_S};font-size:13.5px}}
      .num{{fill:{INK_D};font-size:21px;font-weight:600}}
      .lang{{fill:{INK};font-size:12.5px}}
      .pct{{fill:{INK_F};font-size:11px}}
      .head{{fill:{INK_F};font-size:12px;letter-spacing:2px}}
    </style>
  </defs>
  <rect x="0" y="0" width="600" height="210" rx="0" fill="{PAPER}"/>
  <rect x="0" y="0" width="600" height="210" rx="0" fill="url(#fl)"/>
  <rect x="0" y="0" width="600" height="210" rx="0" fill="url(#in)"/>
  <rect x="0" y="0" width="600" height="210" rx="0" filter="url(#gr)" opacity="0.22" style="mix-blend-mode:multiply"/>
  <rect x="0.75" y="0.75" width="598.5" height="208.5" rx="0" fill="none" stroke="{INK}" stroke-opacity="0.14" stroke-width="1.5"/>
  <g transform="translate(28,30)" fill="none" stroke="{FLAME}" stroke-width="1.7" stroke-linecap="round">
    <g transform="scale(0.72)">
      <path d="M12 2.5 L12 21.5 M3.77 7.25 L20.23 16.75 M20.23 7.25 L3.77 16.75 M12 2.5 l-1.9 2 M12 2.5 l1.9 2 M12 21.5 l-1.9 -2 M12 21.5 l1.9 -2 M20.23 7.25 l-2.7 -0.3 M20.23 7.25 l-0.3 2.7 M3.77 16.75 l2.7 0.3 M3.77 16.75 l0.3 -2.7 M3.77 7.25 l2.7 -0.3 M3.77 7.25 l0.3 2.7 M20.23 16.75 l-2.7 0.3 M20.23 16.75 l-0.3 -2.7"/>
    </g>
  </g>
  <text class="eb" x="48" y="42">GITHUB · STATS</text>
  <text class="head" x="320" y="60">TOP LANGUAGES</text>
  {left}
  {right}
</svg>'''

    with open("stats.svg", "w") as f:
        f.write(svg)
    print("Stats SVG generated (riso).")


if __name__ == "__main__":
    fetch_github_stats()
