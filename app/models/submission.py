from app import db

class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    code = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Submission {self.id} do usuário {self.user_id}>"