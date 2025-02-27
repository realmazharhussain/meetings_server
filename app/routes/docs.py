from flask import Blueprint, abort
from docutils.core import publish_parts
import os

bp = Blueprint('docs', __name__)

def rst_to_html(rst_content):
    parts = publish_parts(source=rst_content, writer_name='html5')
    html_template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Documentation</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css">
    <style>
        :root {
            --max-width: 1000px;
            --font-family: system-ui, -apple-system, "Segoe UI", "Roboto", "Ubuntu",
                "Cantarell", "Noto Sans", sans-serif, "Apple Color Emoji",
                "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
        }
        body { padding: 2rem; }
        main { 
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 1rem;
            background: var(--card-background-color);
            border-radius: 8px;
        }
        pre {
            padding: 1rem;
            border-radius: 4px;
            overflow-x: auto;
        }
        .literal {
            background: var(--card-sectionning-background-color);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <main class="container">
        {content}
    </main>
</body>
</html>
"""
    return html_template.format(content=parts['html_body'])

@bp.route('/docs/<path:filename>')
def serve_docs(filename):
    docs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'docs')
    
    if not filename.endswith(('.rst', '.md')):
        return abort(404)
        
    try:
        with open(os.path.join(docs_dir, filename), 'r', encoding='utf-8') as f:
            content = f.read()
            if filename.endswith('.rst'):
                return rst_to_html(content)
            return abort(404)
    except FileNotFoundError:
        abort(404) 