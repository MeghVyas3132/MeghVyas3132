from datetime import datetime, timedelta
import random

def generate_terminal_logs():
    log_templates = [
        ("INFO", "Pod {service}-{id} started"),
        ("INFO", "Health check passed: {service}"),
        ("DEBUG", "Cache hit: user:{id}"),
        ("INFO", "Request processed: 200 OK ({latency}ms)"),
        ("WARN", "High latency detected: {service}"),
        ("INFO", "Auto-scaling triggered: +{pods} pods"),
        ("INFO", "Database query optimized ({old}ms→{new}ms)"),
        ("INFO", "SSL cert renewed: *.meghvyas.dev"),
        ("DEBUG", "Circuit breaker: CLOSED"),
        ("INFO", "Backup completed: {size} MB"),
        ("INFO", "Deploy rollout: {current}/{total} pods updated"),
        ("INFO", "Metric exported: cpu_usage={cpu}%"),
        ("INFO", "Container started: {service}-{id}"),
        ("DEBUG", "Rate limit check: {requests} req/s"),
        ("INFO", "Load balancer: distributing traffic"),
    ]
    
    services = ["auth-service", "api-gateway", "user-service", "payment-service", "notification-svc"]
    
    current_time = datetime.utcnow()
    logs = []
    
    for i in range(15):
        timestamp = (current_time - timedelta(seconds=i*2)).strftime("%Y-%m-%d %H:%M:%S")
        level, template = random.choice(log_templates)
        
        log_line = template.format(
            service=random.choice(services),
            id=f"{random.randint(1, 9)}{random.choice('abcdef')}{random.randint(1, 9)}{random.choice('abcdef')}{random.randint(1, 9)}",
            latency=random.randint(10, 50),
            pods=random.randint(1, 3),
            old=random.randint(40, 100),
            new=random.randint(10, 25),
            size=random.randint(500, 1000),
            current=random.randint(20, 40),
            total=47,
            cpu=random.randint(70, 95),
            requests=random.randint(5000, 10000)
        )
        
        logs.append((timestamp, level, log_line))
    
    logs.reverse()  # Show most recent at bottom
    
    svg = f'''<svg width="1200" height="400" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <style>
      .terminal-bg {{ fill: #0a0a0a; }}
      .terminal-border {{ fill: none; stroke: #404040; stroke-width: 2; }}
      .terminal-title {{ font: bold 16px 'Courier New', monospace; fill: #ffffff; }}
      .log-text {{ font: 12px 'Courier New', monospace; }}
      .log-info {{ fill: #fdba74; }}
      .log-warn {{ fill: #fcd34d; }}
      .log-debug {{ fill: #a8a29e; }}
      .cursor {{ fill: #fdba74; }}
      @keyframes blink {{
        0%, 50% {{ opacity: 1; }}
        51%, 100% {{ opacity: 0; }}
      }}
      .blinking {{ animation: blink 1s infinite; }}
    </style>
  </defs>
  
  <rect width="1200" height="400" class="terminal-bg"/>
  <rect x="5" y="5" width="1190" height="390" class="terminal-border" rx="8"/>
  
  <!-- Terminal Header -->
  <rect x="15" y="15" width="1170" height="35" fill="#1a1a1a" rx="5"/>
  <text x="30" y="38" class="terminal-title">LIVE SYSTEM LOGS [LAST 60 SECONDS]</text>
  
  <!-- Log Lines -->
  {generate_log_lines(logs)}
  
  <!-- Cursor -->
  <rect x="30" y="370" width="10" height="15" class="cursor blinking"/>
  <text x="45" y="382" class="log-text log-info">[Streaming...]</text>
</svg>'''
    
    with open('terminal-logs.svg', 'w') as f:
        f.write(svg)
    
    print("Terminal logs generated!")

def generate_log_lines(logs):
    y_start = 70
    line_height = 20
    lines = []
    
    for i, (timestamp, level, message) in enumerate(logs):
        y = y_start + i * line_height
        
        color_class = {
            'INFO': 'log-info',
            'WARN': 'log-warn',
            'DEBUG': 'log-debug'
        }.get(level, 'log-info')
        
        lines.append(f'<text x="30" y="{y}" class="log-text {color_class}">[{timestamp}] {level:<6} | {message}</text>')
    
    return '\n  '.join(lines)

if __name__ == "__main__":
    generate_terminal_logs()
