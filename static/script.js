// DOM Elements
const codeInput = document.getElementById('codeInput');
const executeBtn = document.getElementById('executeBtn');
const clearBtn = document.getElementById('clearBtn');
const runTestFileBtn = document.getElementById('runTestFileBtn');
const outputContent = document.getElementById('outputContent');
const outputStats = document.getElementById('outputStats');
const lineNumbers = document.getElementById('lineNumbers');
const exampleCards = document.querySelectorAll('.example-card');

// Update line numbers
function updateLineNumbers() {
    const lines = codeInput.value.split('\n').length;
    lineNumbers.textContent = Array.from({ length: lines }, (_, i) => i + 1).join('\n');
}

// Sync scroll between textarea and line numbers
codeInput.addEventListener('scroll', () => {
    lineNumbers.scrollTop = codeInput.scrollTop;
});

// Update line numbers on input
codeInput.addEventListener('input', updateLineNumbers);

// Execute code
async function executeCode() {
    const code = codeInput.value.trim();

    if (!code) {
        showError('Please enter some code to execute');
        return;
    }

    // Disable button and show loading state
    executeBtn.disabled = true;
    executeBtn.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style="animation: spin 1s linear infinite;">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="2" stroke-dasharray="10 5" fill="none"/>
        </svg>
        Executing...
    `;

    try {
        const response = await fetch('/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code }),
        });

        const data = await response.json();

        if (data.success) {
            showResult(data.result, data.tokens, data.token_list, data.token_values);
        } else {
            showError(data.error, data.tokens, data.token_list, data.token_values);
        }
    } catch (error) {
        showError('Failed to connect to server: ' + error.message);
    } finally {
        // Reset button
        executeBtn.disabled = false;
        executeBtn.innerHTML = `
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M3.333 2.667L12.667 8l-9.334 5.333V2.667z" fill="currentColor"/>
            </svg>
            Execute
        `;
    }
}

// Execute test file
async function executeTestFile() {
    // Disable button and show loading state
    runTestFileBtn.disabled = true;
    const originalText = runTestFileBtn.innerHTML;
    runTestFileBtn.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style="animation: spin 1s linear infinite;">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="2" stroke-dasharray="10 5" fill="none"/>
        </svg>
        Running...
    `;

    try {
        const response = await fetch('/execute_file', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        const data = await response.json();

        // Update editor with the executed code
        if (data.executed_code) {
            codeInput.value = data.executed_code;
            updateLineNumbers();
        }

        if (data.success) {
            showResult(data.result, data.tokens, data.token_list, data.token_values);
        } else {
            showError(data.error, data.tokens, data.token_list, data.token_values);
        }
    } catch (error) {
        showError('Failed to connect to server: ' + error.message);
    } finally {
        // Reset button
        runTestFileBtn.disabled = false;
        runTestFileBtn.innerHTML = originalText;
    }
}

// Show result
// Show result
function showResult(result, tokens, tokenList = [], tokenValues = []) {
    let tokenListHtml = '';
    if (tokenList && tokenList.length > 0) {
        tokenListHtml = `
            <div class="result-label">Token Types</div>
            <div class="result-value" style="font-family: 'Courier New', monospace; word-break: break-all;">
                ${tokenList.map(token => `<span style="background: rgba(6, 182, 212, 0.1); padding: 2px 6px; margin: 2px; border-radius: 4px; display: inline-block;">${escapeHtml(token)}</span>`).join(' ')}
            </div>
        `;
    }

    let tokenValuesHtml = '';
    if (tokenValues && tokenValues.length > 0) {
        tokenValuesHtml = `
            <div class="result-label">Token Values</div>
            <div class="result-value" style="font-family: 'Courier New', monospace; word-break: break-all;">
                ${tokenValues.map(value => `<span style="background: rgba(168, 85, 247, 0.1); padding: 2px 6px; margin: 2px; border-radius: 4px; display: inline-block;">${escapeHtml(value || '—')}</span>`).join(' ')}
            </div>
        `;
    }

    let resultHtml = '';
    if (result) {
        resultHtml = `
            <div class="result-label">Parse Result</div>
            <div class="result-value">${escapeHtml(result)}</div>
        `;
    }

    outputContent.innerHTML = `
        <div class="result-block">
            ${resultHtml}
            
            <div class="result-label">Token Count</div>
            <div class="result-value">${tokens} token${tokens !== 1 ? 's' : ''}</div>
            
            ${tokenListHtml}
            ${tokenValuesHtml}
        </div>
    `;

    outputStats.innerHTML = `
        <span style="color: var(--success);">✓ Success</span>
    `;
}

// Show error
function showError(error, tokens = null, tokenList = [], tokenValues = []) {
    let content = `<div class="error-block">${escapeHtml(error)}</div>`;

    if (tokens !== null && tokens !== undefined) {
        let tokenListHtml = '';
        if (tokenList && tokenList.length > 0) {
            tokenListHtml = `
                <div class="result-label">Token Types</div>
                <div class="result-value" style="font-family: 'Courier New', monospace; word-break: break-all;">
                    ${tokenList.map(token => `<span style="background: rgba(6, 182, 212, 0.1); padding: 2px 6px; margin: 2px; border-radius: 4px; display: inline-block;">${escapeHtml(token)}</span>`).join(' ')}
                </div>
            `;
        }

        let tokenValuesHtml = '';
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
        `;
    }

    outputContent.innerHTML = content;

    outputStats.innerHTML = `
        <span style="color: var(--error);">✗ Error</span>
    `;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Clear editor
function clearEditor() {
    codeInput.value = '';
    updateLineNumbers();
    outputContent.innerHTML = `
        <div class="empty-state">
            <svg width="64" height="64" viewBox="0 0 64 64" fill="none">
                <circle cx="32" cy="32" r="30" stroke="url(#emptyGradient)" stroke-width="2" stroke-dasharray="4 4"/>
                <path d="M32 20v24M20 32h24" stroke="url(#emptyGradient)" stroke-width="2" stroke-linecap="round"/>
                <defs>
                    <linearGradient id="emptyGradient" x1="0" y1="0" x2="64" y2="64">
                        <stop offset="0%" stop-color="#06b6d4" stop-opacity="0.3"/>
                        <stop offset="100%" stop-color="#a855f7" stop-opacity="0.3"/>
                    </linearGradient>
                </defs>
            </svg>
            <p>No output yet</p>
            <span>Execute some code to see results here</span>
        </div>
    `;
    outputStats.innerHTML = '';
    codeInput.focus();
}

// Load example
function loadExample(code) {
    codeInput.value = code;
    updateLineNumbers();
    codeInput.focus();

    // Auto-execute after a short delay
    setTimeout(() => {
        executeCode();
    }, 300);
}

// Event Listeners
executeBtn.addEventListener('click', executeCode);
runTestFileBtn.addEventListener('click', executeTestFile);
clearBtn.addEventListener('click', clearEditor);

// Keyboard shortcuts
codeInput.addEventListener('keydown', (e) => {
    // Ctrl+Enter to execute
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        executeCode();
    }

    // Tab key for indentation
    if (e.key === 'Tab') {
        e.preventDefault();
        const start = codeInput.selectionStart;
        const end = codeInput.selectionEnd;
        codeInput.value = codeInput.value.substring(0, start) + '    ' + codeInput.value.substring(end);
        codeInput.selectionStart = codeInput.selectionEnd = start + 4;
        updateLineNumbers();
    }
});

// Example cards
exampleCards.forEach(card => {
    card.addEventListener('click', () => {
        const code = card.getAttribute('data-code');
        loadExample(code);
    });
});

// Add spin animation for loading state
const style = document.createElement('style');
style.textContent = `
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
`;
document.head.appendChild(style);

// Initialize
updateLineNumbers();
codeInput.focus();
