import requests
import random
from datetime import datetime

USERNAME = "MeghVyas3132"
API_BASE = "https://api.github.com"

def generate_cicd_pipeline():
    # Get latest workflow run
    build_num = random.randint(1800, 1900)
    progress = random.randint(45, 95)
    success_rate = round(92 + random.random() * 6, 1)
    
    current_time = datetime.utcnow().strftime("%H:%M:%S")
    
    # Determine stage statuses based on progress (no emojis)
    stages = [
        ("CODE", "DONE", progress > 15),
        ("TEST", "DONE", progress > 30),
        ("SCAN", "DONE", progress > 45),
        ("BUILD", "DONE" if progress > 60 else "RUNNING", progress > 60),
        ("DEPLOY", "RUNNING" if progress > 75 else "PENDING", progress > 75),
        ("VERIFY", "PENDING", False)
    ]
    
    svg = f'''<svg width="1200" height="280" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a0a0a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1a1a1a;stop-opacity:1" />
    </linearGradient>
    <filter id="greenGlow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feFlood flood-color="#4ade80" flood-opacity="0.4"/>
      <feComposite in2="blur" operator="in"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="yellowGlow">
      <feGaussianBlur stdDeviation="3" result="blur"/>
      <feFlood flood-color="#facc15" flood-opacity="0.4"/>
      <feComposite in2="blur" operator="in"/>
      <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>
      .title {{ font: bold 22px 'Courier New', monospace; fill: #ffffff; }}
      .label {{ font: 14px 'Courier New', monospace; fill: #808080; }}
      .value {{ font: bold 16px 'Courier New', monospace; fill: #e0e0e0; }}
      .stage {{ font: bold 15px 'Courier New', monospace; fill: #e0e0e0; }}
      .status {{ font: bold 12px 'Courier New', monospace; }}
      .status-done {{ fill: #6ee7a0; }}
      .status-running {{ fill: #fde68a; }}
      .status-pending {{ fill: #606060; }}
      .border2 {{ fill: none; stroke: #ffffff; stroke-width: 2; }}
      .panel2 {{ fill: rgba(20, 20, 20, 0.9); stroke: #404040; stroke-width: 1; }}
      .stagebox {{ fill: #1a1a1a; stroke: #404040; stroke-width: 2; }}
      .stagebox-done {{ fill: #1a1a1a; stroke: #4ade80; stroke-width: 2; stroke-opacity: 0.5; }}
      .stagebox-running {{ fill: #1a1a1a; stroke: #facc15; stroke-width: 2; stroke-opacity: 0.5; }}
      .stagebox-pending {{ fill: #1a1a1a; stroke: #404040; stroke-width: 2; }}
    </style>
  </defs>
  
  <rect width="1200" height="280" fill="url(#bgGrad2)"/>
  <rect x="5" y="5" width="1190" height="270" class="border2" rx="8"/>
  
  <!-- Header -->
  <text x="20" y="35" class="title">CONTINUOUS DEPLOYMENT PIPELINE</text>
  <text x="20" y="55" class="label">BUILD #{build_num} | branch: main | commit: a7f3c2d | status: DEPLOYING</text>
  
  <!-- Pipeline Stages -->
  <g id="pipeline">
    {generate_stages(stages)}
  </g>
  
  <!-- Progress Bar -->
  <text x="20" y="185" class="label">Progress:</text>
  <rect x="120" y="172" width="1050" height="20" fill="#1a1a1a" stroke="#404040" stroke-width="2" rx="10"/>
  <rect x="120" y="172" width="{int(1050 * progress / 100)}" height="20" fill="#ffffff" rx="10"/>
  <text x="1100" y="187" class="value">{progress}%</text>
  
  <text x="120" y="210" class="label">ETA: {random.randint(1, 5)}m {random.randint(10, 59)}s remaining</text>
  
  <!-- Current Stage Info -->
  <rect x="20" y="220" width="1160" height="50" class="panel2" rx="5"/>
  <text x="35" y="240" class="title">CURRENT STAGE: Deploying to prod-cluster-01</text>
  <text x="35" y="258" class="label">&gt; Rolling update in progress... | Pods: {random.randint(10, 20)}/47 updated | Health checks: PASSING</text>
  
</svg>'''
    
    with open('cicd-pipeline.svg', 'w') as f:
        f.write(svg)
    
    print("CI/CD Pipeline generated!")

def generate_stages(stages):
    x_start = 60
    y = 100
    stage_width = 160
    stage_height = 50
    gap = 30
    
    stage_svgs = []
    
    for i, (name, status, completed) in enumerate(stages):
        x = x_start + i * (stage_width + gap)
        
        # Stage box with colored glow based on status
        if status == "DONE":
            box_class = "stagebox-done"
            glow_filter = 'filter="url(#greenGlow)"'
        elif status == "RUNNING":
            box_class = "stagebox-running"
            glow_filter = 'filter="url(#yellowGlow)"'
        else:
            box_class = "stagebox-pending"
            glow_filter = ''
        
        stage_svgs.append(f'<rect x="{x}" y="{y}" width="{stage_width}" height="{stage_height}" class="{box_class}" {glow_filter}/>')
        
        # Stage name
        stage_svgs.append(f'<text x="{x + stage_width//2}" y="{y + 22}" class="stage" text-anchor="middle">{name}</text>')
        
        # Status text with color
        if status == "DONE":
            status_class = "status status-done"
        elif status == "RUNNING":
            status_class = "status status-running"
        else:
            status_class = "status status-pending"
        stage_svgs.append(f'<text x="{x + stage_width//2}" y="{y + 40}" class="{status_class}" text-anchor="middle">{status}</text>')
        
        # Arrow to next stage
        if i < len(stages) - 1:
            arrow_x = x + stage_width + 5
            stage_svgs.append(f'<line x1="{arrow_x}" y1="{y + stage_height//2}" x2="{arrow_x + gap - 10}" y2="{y + stage_height//2}" stroke="#ffffff" stroke-width="3"/>')
            stage_svgs.append(f'<polygon points="{arrow_x + gap - 10},{y + stage_height//2} {arrow_x + gap - 18},{y + stage_height//2 - 5} {arrow_x + gap - 18},{y + stage_height//2 + 5}" fill="#ffffff"/>')
    
    return '\n    '.join(stage_svgs)

if __name__ == "__main__":
    generate_cicd_pipeline()
