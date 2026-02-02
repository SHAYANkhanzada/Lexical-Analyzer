# Update header with team names
with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the status badge section
old_status = '''            <div class="status-badge">
                <span class="status-dot"></span>
                <span>Ready</span>
            </div>'''


content = content.replace(old_status, new_status)

# Write back
with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated header successfully!")
