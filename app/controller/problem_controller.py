from flask import Blueprint, render_template
from app.models.problem import Problem

problem_bp = Blueprint('problem', __name__)

@problem_bp.route('/problems')
def list_problems():
    # Busca todos os problemas no banco
    problems = Problem.query.all()
    return render_template('problems.html', problems=problems)