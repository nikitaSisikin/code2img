from flask import (
    Flask, 
    render_template, 
    session,
    redirect,
    request,
    url_for,
)
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import Python3Lexer
from pygments.styles import get_all_styles

# Create a Flask application instance
app = Flask(__name__)

# Set a secret key for session management
app.secret_key = "7eece3a4f7d9f421394148f606110eec2c15d1de6bff7d7e507f96d63318169d"

# Placeholder code for initial session value
placeholder_code = "print('Hello, World!')"
# Default style
default_style = "monokai"

# Define a route for handling code-related actions
@app.route("/", methods=["GET"])
def code():
    # If the "code" key is not in the session, initialize it with the placeholder code
    if session.get("code") is None:
        session["code"] = placeholder_code
    # get code lines
    lines = session["code"].split("\n")
    # Prepare the context for rendering the template
    context = {
        "message": "Paste your code here 🐍",
        "code": session["code"],
        "num_lines": len(lines),
        "max_chars": len(max(lines, key=len)),
    }
    
    # Render the 'code_input.html' template with the provided context
    return render_template("code_input.html", **context)

# Define a route for saving the code
@app.route("/save_code", methods=["POST"])
def save_code():
    # Retrieve the code from the form submitted in the request
    session["code"] = request.form.get("code")
    
    # Redirect to the '/code' route to display the updated code input page
    return redirect(url_for("code"))

# Define a route for resetting the session
@app.route("/reset_session", methods=["POST"])
def reset_session():
    # Clear the session data
    session.clear()
    
    # Set the "code" key in the session to the placeholder code
    session["code"] = placeholder_code
    
    # Redirect to the '/save_code' route to display the code input page
    return redirect(url_for("code"))

@app.route("/style", methods=["GET"])
def style():
    if session.get("style") is None:
        session["style"] = default_style
    formatter = HtmlFormatter(style=session["style"])
    context = {
        "message": "Select your style 🦋",
        "all_styles": list(get_all_styles()),
        "style_definitions": formatter.get_style_defs(),
        "style_bg_color": formatter.style.background_color,
        "highlited_code": highlight(
            session["code"], Python3Lexer(), formatter
        )
    }
    return render_template("style_selection.html", **context)

@app.route("/save_style", methods=["POST"])
def save_style():
    session["style"] = request.form.get("style")
    return redirect(url_for("style"))