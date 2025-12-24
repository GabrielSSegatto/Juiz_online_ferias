from flask import Blueprint, render_template
from app.service.ranking_service import get_ranking

ranking_bp = Blueprint('ranking', __name__)

@ranking_bp.route('/ranking',methods = ['GET'])
def get_ranking_controller():

    users = get_ranking()

    return render_template("ranking.html", users = users)
