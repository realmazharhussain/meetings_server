from flask import Blueprint, send_file, request
from io import BytesIO

bp = Blueprint('static', __name__)

def create_placeholder_svg(width=500, height=300):
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{width}" height="{height}" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <rect width="100%" height="100%" fill="#F5F5F5"/>
    <text x="50%" y="50%" font-family="Arial" font-size="24" fill="#999" text-anchor="middle" dy=".3em">
        {width} × {height}
    </text>
</svg>'''
    return BytesIO(svg.encode())

@bp.route('/placeholder.svg')
def placeholder():
    width = int(request.args.get('width', 500))
    height = int(request.args.get('height', 300))
    svg_io = create_placeholder_svg(width, height)
    svg_io.seek(0)
    return send_file(svg_io, mimetype='image/svg+xml') 