import re

# Read the file
with open('static/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace showResult function signature
content = re.sub(
    r'function showResult\(result, tokens, tokenList = \[\]\)',
    'function showResult(result, tokens, tokenList = [], tokenValues = [])',
    content
)

# Replace showError function signature
content = re.sub(
    r'function showError\(error, tokens = null, tokenList = \[\]\)',
    'function showError(error, tokens = null, tokenList = [], tokenValues = [])',
    content
)

# Add token values display in showResult
content = re.sub(
    r'(let tokenListHtml = \'\';\s+if \(tokenList && tokenList\.length > 0\) \{[^}]+\})',
    r'''\1
    
    let tokenValuesHtml = '';
    if (tokenValues && tokenValues.length > 0) {
        tokenValuesHtml = `
            <div class="result-label">Token Values</div>
            <div class="result-value" style="font-family: 'Courier New', monospace; word-break: break-all;">
                ${tokenValues.map(value => `<span style="background: rgba(168, 85, 247, 0.1); padding: 2px 6px; margin: 2px; border-radius: 4px; display: inline-block;">${escapeHtml(value || '—')}</span>`).join(' ')}
            </div>
        `;
    }''',
    content,
    count=1
)

# Change "Token List" to "Token Types"
content = content.replace('<div class="result-label">Token List</div>', '<div class="result-label">Token Types</div>')

# Add tokenValuesHtml to output in showResult
content = re.sub(
    r'(\$\{tokenListHtml\}\s+</div>)',
    r'${tokenListHtml}\n            ${tokenValuesHtml}\n        </div>',
    content,
    count=1
)

# Write back
with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated script.js successfully!")
