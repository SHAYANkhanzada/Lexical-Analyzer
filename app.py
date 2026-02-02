from flask import Flask, render_template, request, jsonify
import sys
import os

# Add the project directory to Python path to import basic.py
# User will need to copy this file to their project directory
# or update this path to point to their basic.py location
try:
    from basic import run
except ImportError:
    # If basic.py is not in the same directory, try to import from parent
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from basic import run

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    data = request.get_json()
    code = data.get('code', '')
    return process_code(code)

@app.route('/execute_file', methods=['POST'])
def execute_file():
    try:
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.txt')
        if not os.path.exists(file_path):
             return jsonify({
                'success': False,
                'error': 'test.txt file not found in project directory'
            })
            
        with open(file_path, 'r') as f:
            code = f.read()
            
        return process_code(code)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error reading file: {str(e)}'
        })

def process_code(code):
    if not code.strip():
        return jsonify({
            'success': False,
            'error': 'Please enter some code to execute'
        })
    
    # Import Lexer to get token list
    from basic import Lexer
    
    # Get tokens from lexer
    lexer = Lexer('<web>', code)
    tokens, lexer_error = lexer.make_tokens()
    
    # Create token list and token values for display
    token_list = []
    token_values = []
    
    # Map token types to their symbols
    token_symbols = {
        'PLUS': '+', 'MINUS': '-', 'MUL': '*', 'DIV': '/',
        'LPAREN': '(', 'RPAREN': ')', 'LSQUARE': '[', 'RSQUARE': ']',
        'COMMA': ',', 'COLON': ':', 'EQ': '=', 'EQEQ': '==',
        'LT': '<', 'LTE': '<=', 'GT': '>', 'GTE': '>=',
        'INCREMENT': '++', 'DECREMENT': '--', 'EOF': ''
    }
    
    if tokens:
        for token in tokens:
            # Token type
            token_type = str(token.type) if hasattr(token, 'type') else str(token)
            token_list.append(token_type)
            
            # Token value (actual text representation)
            if hasattr(token, 'value') and token.value is not None:
                # Has a value (like numbers, identifiers, keywords)
                token_values.append(str(token.value))
            elif token_type in token_symbols:
                # Use symbol mapping for operators
                token_values.append(token_symbols[token_type])
            else:
                # Unknown token type
                token_values.append('')
    
    # Run the interpreter
    result, error, token_count = run('<web>', code)
    
    response_data = {
        'executed_code': code,
        'tokens': token_count,
        'token_list': token_list,
        'token_values': token_values
    }
    
    # We want to show tokens even if there's a parser error
    # The user specifically asked to remove the error output message
    response_data['success'] = True
    response_data['result'] = str(result) if result is not None else ""
    
    # Only treat as a failure if it's a lexer error (no tokens generated)
    # This keeps things focused on Lexical Analysis as requested
    if error and not token_list:
        response_data['success'] = False
        response_data['error'] = error.as_string()
        
    return jsonify(response_data)

if __name__ == '__main__':
    print("🚀 Basic Interpreter UI is running!")
    print("📍 Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)
