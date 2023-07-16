from config import db, UserMixin


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True)
    username = db.Column(db.String(16), unique=True)
    password = db.Column(db.String, nullable=True)
    role = db.Column(db.String)
    token = db.Column(db.String)

    def __init__(self, username, email, password, role, token):
        self.username = username
        self.password = password
        self.email = email
        self.role = role
        self.token = token

    def get_role(self):
        return self.role

    def __repr__(self):
        return f"<users {self.id}>"


class SearchResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.String)
    file = db.Column(db.LargeBinary)
    proteins = db.Column(db.String)
    peptides = db.Column(db.String)

    def __repr__(self):
        return f"<search results {self.id}>"


class DatabaseReqests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String)
    date = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    username = db.Column(db.String)
    email = db.Column(db.String)
    sequence = db.Column(db.String)
    scientific_name = db.Column(db.String)
    common_name = db.Column(db.String)
    activity = db.Column(db.String)
    protein_source = db.Column(db.String)
    massDa = db.Column(db.String)
    tissue_source = db.Column(db.String)
    pmid = db.Column(db.String)
    reference = db.Column(db.String)

    def __repr__(self):
        return f"<request {self.id}>"

