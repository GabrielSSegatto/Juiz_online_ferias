from app.models.user import User

def get_ranking(limit = 50):

    return User.query.order_by(User.points.desc()).limit(limit).all()