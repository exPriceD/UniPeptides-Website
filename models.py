from config import db, UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(128), nullable=True)
    role = db.Column(db.String(10))
    token = db.Column(db.String(50))
    token_date = db.Column(db.DateTime)

    def __init__(self, username, email, password, role, token, token_date):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.token = token
        self.token_date = token_date

    def get_role(self):
        return self.role

    def __repr__(self):
        return f"<users {self.id}>"


class SearchResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.String(25))
    file = db.Column(db.LargeBinary)
    proteins = db.Column(db.String(65535))
    peptides = db.Column(db.String(65535))

    def __repr__(self):
        return f"<search results {self.id}>"


class DatabaseReqests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20))
    date = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    username = db.Column(db.String(16))
    email = db.Column(db.String(64))
    sequence = db.Column(db.String(100))
    scientific_name = db.Column(db.String(100))
    common_name = db.Column(db.String(100))
    activity = db.Column(db.String(100))
    protein_source = db.Column(db.String(100))
    massDa = db.Column(db.String(100))
    tissue_source = db.Column(db.String(100))
    pmid = db.Column(db.String(30))
    reference = db.Column(db.String(1000))

    def __repr__(self):
        return f"<request {self.id}>"



