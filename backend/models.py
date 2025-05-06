from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_projects = db.Table(
    'user_projects',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    projects = db.relationship('Project', secondary=user_projects, back_populates='users')

    def __repr__(self):
        return f"<User {self.name}>"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    picture = db.Column(db.String(255), nullable=True)

    # Colonnes additionnelles
    client = db.Column(db.String(100))
    chef = db.Column(db.String(100))
    statut = db.Column(db.String(50))
    budget = db.Column(db.Integer)
    debut = db.Column(db.String(20))  # Peut être db.Date
    fin = db.Column(db.String(20))    # Peut être db.Date
    progression = db.Column(db.Integer)

    users = db.relationship('User', secondary=user_projects, back_populates='projects')
    visas = db.relationship('Visa', backref='project', lazy=True)

    # 🆕 Nouveaux liens
    steps = db.relationship('Step', backref='project', cascade="all, delete-orphan", order_by="Step.order", lazy=True)

    def __repr__(self):
        return f"<Project {self.name}>"

class Step(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, nullable=False)  # Ordre d’affichage
    validated = db.Column(db.Boolean, default=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    # Lien sous-étapes
    substeps = db.relationship('SubStep', backref='step', cascade="all, delete-orphan", order_by="SubStep.order", lazy=True)

    def __repr__(self):
        return f"<Step {self.title}>"

class SubStep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(255), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    validated = db.Column(db.Boolean, default=False)
    step_id = db.Column(db.Integer, db.ForeignKey('step.id'), nullable=False)

    def __repr__(self):
        return f"<SubStep {self.label}>"

class Visa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(120))
    objet = db.Column(db.String(50))
    specialite = db.Column(db.String(20))
    type_doc = db.Column(db.String(10))
    chrono = db.Column(db.String(20))
    indice_ged = db.Column(db.String(10))
    discipline = db.Column(db.String(10))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    def __repr__(self):
        return f"<Visa {self.titre}>"
