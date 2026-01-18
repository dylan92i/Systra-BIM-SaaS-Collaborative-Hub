import os

from flask import Blueprint, request, jsonify, current_app, session, send_from_directory
from models import db, User, Project, Visa, Step, SubStep
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from bim_processor import *

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()



@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Check for required fields
        if not data or not all(k in data for k in ('name', 'email', 'password')):
            current_app.logger.warning("Missing data in registration request.")
            return jsonify({'message': 'All fields (name, email, password) are required.'}), 400

        # Check if the email is already in use
        if User.query.filter_by(email=data['email']).first():
            current_app.logger.info(f"Registration attempt with already used email: {data['email']}")
            return jsonify({'message': 'This email is already taken.'}), 409

        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_user = User(name=data['name'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info(f"New user created: {data['email']}")

        return jsonify({'message': 'User created!'}), 201

    except Exception as e:
        current_app.logger.error(f"Error during registration: {e}")
        return jsonify({'message': 'Server error during registration.'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({'message': 'Email and password are required.'}), 400

        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            # ENREGISTRE EN SESSION
            session['user_id'] = user.id
            session['user_name'] = user.name
            current_app.logger.info(f"User logged in: {user.email}")
            return jsonify({'message': 'Login successful!', 'user': user.name}), 200
        else:
            return jsonify({'message': 'Invalid credentials.'}), 401

    except Exception as e:
        return jsonify({'message': 'Server error during login.'}), 500

@auth_bp.route('/get_current_user', methods=['GET'])
def get_current_user():
    if 'user_name' in session:
        return jsonify({'name': session['user_name']}), 200
    else:
        return jsonify({'message': 'Not logged in'}), 401

@auth_bp.route('/get_all_user_names', methods=['GET'])
def get_all_user_names():
    if 'user_name' not in session:
        return jsonify({'message': 'Unauthorized – please log in.'}), 401

    try:
        users = User.query.with_entities(User.name).all()
        names = [user.name for user in users]
        return jsonify(names), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching user names: {e}")
        return jsonify({'message': 'Server error while fetching user names'}), 500

# Project Sector

@auth_bp.route('/add_project', methods=['POST'])
def add_project():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized – please log in.'}), 401

    try:
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        picture = data.get('picture', '')
        user_ids = data.get('user_ids', [])

        if not name:
            return jsonify({'message': 'Project name is required.'}), 400

        # Créer le projet
        new_project = Project(name=name, description=description, picture=picture)

        # Toujours ajouter l'utilisateur connecté/comme créateur du projet
        creator = User.query.get(session['user_id'])
        new_project.users.append(creator)

        # Ajouter les autres utilisateurs si user_ids présents (en évitant doublon)
        if user_ids:
            users_to_add = User.query.filter(User.id.in_(user_ids)).all()
            for user in users_to_add:
                if user not in new_project.users:
                    new_project.users.append(user)

        db.session.add(new_project)
        db.session.commit()

        current_app.logger.info(f"New project created: {name} by user {creator.email}")
        return jsonify({'message': 'Project created successfully!'}), 201

    except Exception as e:
        current_app.logger.error(f"Error creating project: {e}")
        return jsonify({'message': 'Server error while creating project.'}), 500

@auth_bp.route('/upload_project_image', methods=['POST'])
def upload_project_image():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized – please log in.'}), 401

    if 'image' not in request.files:
        return jsonify({'message': 'No image part in request.'}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({'message': 'No image selected for uploading.'}), 400

    # Nettoie le nom du fichier pour éviter les caractères spéciaux
    filename = secure_filename(image.filename)
    upload_folder = os.path.join(current_app.root_path, 'static', 'project_picture')

    # Crée le dossier s’il n’existe pas
    os.makedirs(upload_folder, exist_ok=True)

    # Chemin complet pour le stockage
    filepath = os.path.join(upload_folder, filename)
    image.save(filepath)

    return jsonify({
        'message': 'Image uploaded successfully!',
        'image_url': filename
    }), 201

@auth_bp.route('/get_my_projects', methods=['GET'])
def get_my_projects():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized – please log in.'}), 401

    try:
        user = User.query.get(session['user_id'])
        # Liste des projets associés à ce user
        projects = user.projects  # ou user.projects si bonne relation définie

        result = []
        for project in projects:
            result.append({
                'id': project.id,
                'name': project.name,
                'description': project.description,
                'picture': project.picture
            })

        return jsonify(result), 200

    except Exception as e:
        current_app.logger.error(f"Error fetching user projects: {e}")
        return jsonify({'message': 'Server error while fetching user projects.'}), 500

@auth_bp.route('/get_ressource/<ressource_name>', methods=['GET'])
def get_ressource(ressource_name):
    # Vérifie que l'utilisateur est connecté
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized – please log in.'}), 401

    # Liste blanche des ressources accessibles (modifiable selon les besoins)
    allowed_resources = [
        'create_project.jpg',
        'another_image.png',
        # Ajouter d'autres fichiers ici
    ]

    # Sécurité : vérifier que la ressource demandée est dans la liste blanche
    if ressource_name not in allowed_resources:
        return jsonify({'message': 'Unauthorized or resource not found.'}), 403

    images_folder = os.path.join(current_app.root_path, 'static', 'ressource')

    try:
        return send_from_directory(images_folder, ressource_name)
    except Exception as e:
        current_app.logger.error(f"Error sending resource {ressource_name}: {e}")
        return jsonify({'message': 'Error serving resource.'}), 500

@auth_bp.route('/get_project_picture', methods=['GET'])
def get_project_picture():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized – please log in.'}), 401

    picture_name = request.args.get('picture_name')

    if not picture_name:
        return jsonify({'message': 'Picture name is required.'}), 400

    user = User.query.get(session['user_id'])

    # Vérifie si l'image est dans un des projets de l'utilisateur
    project = Project.query \
        .join(Project.users) \
        .filter(User.id == user.id, Project.picture == picture_name) \
        .first()

    if not project:
        return jsonify({'message': 'Access denied or picture does not exist for this user.'}), 403

    # Dossier où tes images sont stockées 
    images_folder = os.path.join(current_app.root_path, 'static', 'project_picture')

    try:
        return send_from_directory(images_folder, picture_name)
    except Exception as e:
        current_app.logger.error(f"Error sending image {picture_name}: {e}")
        return jsonify({'message': 'Error serving image.'}), 500

# --------- ROUTE : LISTER LES FICHIERS/DOSSIERS ---------
@auth_bp.route('/get_my_files', methods=['GET'])
def get_my_files():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    folder = request.args.get('folder', '').strip('/')
    folder = secure_user_path(folder)
    user_root = get_user_folder()
    if not user_root:
        return jsonify({'message': 'User folder problem.'}), 500
    base_folder = os.path.join(user_root, folder)
    os.makedirs(base_folder, exist_ok=True)  # Crée le dossier si besoin

    items = []
    try:
        for entry in os.listdir(base_folder):
            full_path = os.path.join(base_folder, entry)
            items.append({
                "name": entry,
                "is_dir": os.path.isdir(full_path),
                "size": os.path.getsize(full_path) if os.path.isfile(full_path) else None
            })
        return jsonify(items), 200
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'message': 'Error reading folder.'}), 500

# --------- ROUTE : UPLOAD (ENVOI) D'UN FICHIER ---------
@auth_bp.route('/upload_file', methods=['POST'])
def upload_file():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    user_root = get_user_folder()
    if not user_root:
        return jsonify({'message': 'User folder problem.'}), 500
    folder = secure_user_path(request.form.get('folder', '').strip('/'))
    base_folder = os.path.join(user_root, folder)
    os.makedirs(base_folder, exist_ok=True)  # Crée le dossier si besoin

    if 'file' not in request.files:
        return jsonify({'message': 'No file part.'}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)
    dest_path = os.path.join(base_folder, filename)
    file.save(dest_path)
    return jsonify({'message': 'File uploaded successfully.'}), 200

# --------- ROUTE : CREER UN DOSSIER ---------
@auth_bp.route('/create_folder', methods=['POST'])
def create_folder():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    parent = secure_user_path(data.get('parent', '').strip('/'))
    name = secure_filename(data.get('name', '').strip())

    if not name:
        return jsonify({'message': 'No folder name.'}), 400

    user_root = get_user_folder()
    if not user_root:
        return jsonify({'message': 'User folder problem.'}), 500
    new_folder_path = os.path.join(user_root, parent, name)

    try:
        os.makedirs(new_folder_path, exist_ok=False)
        return jsonify({'message': 'Folder created successfully.'}), 200
    except FileExistsError:
        return jsonify({'message': 'Folder already exists.'}), 400
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'message': 'Error creating folder.'}), 500

# --------- ROUTE : SUPPRIMER UN FICHIER/DOSSIER ---------
@auth_bp.route('/delete', methods=['POST'])
def delete_item():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    data = request.get_json()
    rel_path = secure_user_path(data.get('path', '').strip('/'))
    user_root = get_user_folder()
    if not user_root:
        return jsonify({'message': 'User folder problem.'}), 500
    target_path = os.path.join(user_root, rel_path)

    try:
        if os.path.isdir(target_path):
            import shutil
            shutil.rmtree(target_path)
        elif os.path.isfile(target_path):
            os.remove(target_path)
        else:
            return jsonify({'message': 'Path not found.'}), 404
        return jsonify({'message': 'Deleted successfully.'}), 200
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'message': 'Error deleting.'}), 500

# --------- ROUTE : TELECHARGER UN FICHIER ---------
@auth_bp.route('/download', methods=['GET'])
def download_file():
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401

    file_path = secure_user_path(request.args.get('path', '').strip('/'))
    user_root = get_user_folder()
    if not user_root:
        return jsonify({'message': 'User folder problem.'}), 500
    dir_name, filename = os.path.split(file_path)
    base_folder = os.path.join(user_root, dir_name)
    try:
        return send_from_directory(base_folder, filename, as_attachment=True)
    except Exception as e:
        current_app.logger.error(str(e))
        return jsonify({'message': 'File not found.'}), 404

# PROJECT DASH BOARD (utilisation du nom au lieu de l'id)
@auth_bp.route('/main/project/<string:project_name>', methods=['GET'])
def get_project_detail_by_name(project_name):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized – please log in.'}), 401

    p = Project.query.filter_by(name=project_name).first_or_404()
    visas = []
    for v in p.visas:
        visas.append({
            "id": v.id,
            "titre": v.titre,
            "objet": v.objet,
            "specialite": v.specialite,
            "type_doc": v.type_doc,
            "chrono": v.chrono,
            "indice_ged": v.indice_ged,
            "discipline": v.discipline,
        })
    result = {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "client": p.client,
        "chef": p.chef,
        "statut": p.statut,
        "budget": p.budget,
        "debut": p.debut,
        "fin": p.fin,
        "progression": p.progression,
        "picture": p.picture,
        "visas": visas
    }
    return jsonify(result), 200

@auth_bp.route('/update_project/<int:project_id>', methods=['PUT'])
def update_project(project_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized – please log in.'}), 401

    p = Project.query.get_or_404(project_id)
    data = request.get_json()

    # Mets à jour chaque champ si présent dans data
    for field in ['name', 'description', 'client', 'chef', 'statut', 'budget', 'debut', 'fin', 'progression', 'picture']:
        if field in data:
            setattr(p, field, data[field])
    db.session.commit()
    return jsonify({'message': 'Project updated'}), 200

@auth_bp.route('/project/<int:project_id>/add_visa', methods=['POST'])
def add_visa(project_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized – please log in.'}), 401

    p = Project.query.get_or_404(project_id)
    data = request.get_json()
    v = Visa(
        titre = data.get("titre", ""),
        objet = data.get("objet", ""),
        specialite = data.get("specialite", ""),
        type_doc = data.get("type_doc", ""),
        chrono = data.get("chrono", ""),
        indice_ged = data.get("indice_ged", ""),
        discipline = data.get("discipline", ""),
        project_id = p.id
    )
    db.session.add(v)
    db.session.commit()
    return jsonify({'message': 'Visa added'}), 201

# --------- ÉTAPES (Step) ---------

@auth_bp.route('/project/<int:project_id>/steps', methods=['GET'])
def get_steps(project_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    steps = Step.query.filter_by(project_id=project_id).order_by(Step.order).all()
    result = []
    for step in steps:
        substeps = [
            {
                "id": sub.id,
                "label": sub.label,
                "order": sub.order,
                "validated": sub.validated
            } for sub in step.substeps
        ]
        result.append({
            "id": step.id,
            "title": step.title,
            "description": step.description,
            "order": step.order,
            "validated": step.validated,
            "substeps": substeps
        })
    return jsonify(result), 200

@auth_bp.route('/project/<int:project_id>/steps', methods=['POST'])
def add_step(project_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    last_order = db.session.query(db.func.max(Step.order)).filter_by(project_id=project_id).scalar() or 0
    step = Step(
        title=data.get("title", "Nouvelle étape"),
        description=data.get("description", ""),
        order=last_order + 1,
        validated=False,
        project_id=project_id
    )
    db.session.add(step)
    db.session.commit()
    return jsonify({'id': step.id, 'message': 'Step created'}), 201

@auth_bp.route('/step/<int:step_id>', methods=['PUT'])
def update_step(step_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    step = Step.query.get_or_404(step_id)
    data = request.get_json()
    # Modifie les champs reçus
    if "title" in data: step.title = data["title"]
    if "description" in data: step.description = data["description"]
    if "validated" in data: step.validated = bool(data["validated"])
    if "order" in data: step.order = int(data["order"])
    db.session.commit()
    return jsonify({'message': 'Step updated'}), 200

@auth_bp.route('/step/<int:step_id>', methods=['DELETE'])
def delete_step(step_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    step = Step.query.get_or_404(step_id)
    db.session.delete(step)
    db.session.commit()
    return jsonify({'message': 'Step deleted'}), 200

# --------- SOUS-ÉTAPES (SubStep) ---------

@auth_bp.route('/step/<int:step_id>/substeps', methods=['POST'])
def add_substep(step_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    data = request.get_json()
    last_order = db.session.query(db.func.max(SubStep.order)).filter_by(step_id=step_id).scalar() or 0
    substep = SubStep(
        label=data.get("label", "Nouvelle sous-étape"),
        order=last_order + 1,
        validated=False,
        step_id=step_id
    )
    db.session.add(substep)
    db.session.commit()
    return jsonify({'id': substep.id, 'message': 'Substep created'}), 201

@auth_bp.route('/substep/<int:substep_id>', methods=['PUT'])
def update_substep(substep_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    substep = SubStep.query.get_or_404(substep_id)
    data = request.get_json()
    # Modifie les champs reçus
    if "label" in data: substep.label = data["label"]
    if "validated" in data: substep.validated = bool(data["validated"])
    if "order" in data: substep.order = int(data["order"])
    db.session.commit()
    return jsonify({'message': 'Substep updated'}), 200

@auth_bp.route('/substep/<int:substep_id>', methods=['DELETE'])
def delete_substep(substep_id):
    if 'user_id' not in session:
        return jsonify({'message': 'Unauthorized'}), 401
    substep = SubStep.query.get_or_404(substep_id)
    db.session.delete(substep)
    db.session.commit()
    return jsonify({'message': 'Substep deleted'}), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200

