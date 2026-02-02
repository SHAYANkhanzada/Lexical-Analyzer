# Update header with team names
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the status badge section
old_status = '''            <div class="status-badge">
                <span class="status-dot"></span>
                <span>Ready</span>
            </div>'''

new_status = '''            <div class="status-badge" style="display: flex; flex-direction: column; align-items: flex-end; gap: 0.25rem;">
                <div style="font-size: 0.875rem; font-weight: 500;">Shayan (14958), Zarrar (15162)</div>
                <div style="font-size: 0.875rem; font-weight: 500;">Aliya (13604), Somia (10657)</div>
            </div>'''

content = content.replace(old_status, new_status)

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated header successfully!")
