# Fix the broken script.js
with open('static/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find and fix the broken showResult function (lines 72-110)
fixed_lines = lines[:72]  # Keep everything before showResult

# Add corrected showResult function
fixed_lines.extend([
    '// Show result\n',
    'function showResult(result, tokens, tokenList = [], tokenValues = []) {\n',
    '    let tokenListHtml = \'\';\n',
    '    if (tokenList && tokenList.length > 0) {\n',
    '        tokenListHtml = `\n',
    '            <div class="result-label">Token Types</div>\n',
    '            <div class="result-value" style="font-family: \'Courier New\', monospace; word-break: break-all;">\n',
    '                ${tokenList.map(token => `<span style="background: rgba(6, 182, 212, 0.1); padding: 2px 6px; margin: 2px; border-radius: 4px; display: inline-block;">${escapeHtml(token)}</span>`).join(\' \')}\n',
    '            </div>\n',
    '        `;\n',
    '    }\n',
    '    \n',
    '    let tokenValuesHtml = \'\';\n',
    '    if (tokenValues && tokenValues.length > 0) {\n',
    '        tokenValuesHtml = `\n',
    '            <div class="result-label">Token Values</div>\n',
    '            <div class="result-value" style="font-family: \'Courier New\', monospace; word-break: break-all;">\n',
    '                ${tokenValues.map(value => `<span style="background: rgba(168, 85, 247, 0.1); padding: 2px 6px; margin: 2px; border-radius: 4px; display: inline-block;">${escapeHtml(value || \'—\')}</span>`).join(\' \')}\n',
    '            </div>\n',
    '        `;\n',
    '    }\n',
    '\n',
    '    outputContent.innerHTML = `\n',
    '        <div class="result-block">\n',
    '            <div class="result-label">Parse Result</div>\n',
    '            <div class="result-value">${escapeHtml(result)}</div>\n',
    '            \n',
    '            <div class="result-label">Token Count</div>\n',
    '            <div class="result-value">${tokens} token${tokens !== 1 ? \'s\' : \'\'}</div>\n',
    '            \n',
    '            ${tokenListHtml}\n',
    '            ${tokenValuesHtml}\n',
    '        </div>\n',
    '    `;\n',
    '    \n',
    '    outputStats.innerHTML = `\n',
    '        <span style="color: var(--success);">✓ Success</span>\n',
    '    `;\n',
    '}\n',
    '\n',
])

# Add the rest of the file from line 111 onwards
fixed_lines.extend(lines[111:])

# Write back
with open('static/script.js', 'w', encoding='utf-8') as f:
    f.writelines(fixed_lines)

print("Fixed script.js successfully!")
