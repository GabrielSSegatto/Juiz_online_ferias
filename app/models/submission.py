from app import db
from datetime import datetime

class Submission(db.Model):

    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(30), nullable = False, default="PENDING")
    language = db.Column(db.String(30), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"), nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    code = db.Column(db.Text, nullable = False)
    user = db.relationship("User", backref="submissions")
    problem = db.relationship("Problem", backref="submissions")


