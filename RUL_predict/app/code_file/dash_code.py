from flask import Blueprint, render_template

dash_bp = Blueprint('dashboard', __name__)

@dash_bp.route('/dashboard')
def dash_board():
    return render_template('index4.html'), 200
    