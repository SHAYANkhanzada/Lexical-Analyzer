# Fix showError function to add token values display
with open('static/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the showError function
old_error_func = '''        content += `
            <div style="margin-top: 1rem;">
                <div class="result-label">Token Count</div>
                <div class="result-value">${tokens} token${tokens !== 1 ? 's' : ''}</div>
                ${tokenListHtml}
            </div>
        `;'''

new_error_func = '''        let tokenValuesHtml = '';
        if (tokenValues && tokenValues.length > 0) {
            tokenValuesHtml = `
                <div class="result-label">Token Values</div>
                <div class="result-value" style="font-family: 'Courier New', monospace; word-break: break-all;">
                    ${tokenValues.map(value => `<span style="background: rgba(168, 85, 247, 0.1); padding: 2px 6px; margin: 2px; border-radius: 4px; display: inline-block;">${escapeHtml(value || '—')}</span>`).join(' ')}
                </div>
            `;
        }

        content += `
            <div style="margin-top: 1rem;">
                <div class="result-label">Token Count</div>
                <div class="result-value">${tokens} token${tokens !== 1 ? 's' : ''}</div>
                ${tokenListHtml}
                ${tokenValuesHtml}
            </div>
        `;'''

content = content.replace(old_error_func, new_error_func)

# Write back
with open('static/script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed showError function successfully!")
