import sqlite3
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

conn = sqlite3.connect('systra_platform.db')
cursor = conn.cursor()

# Informations pour Dylan
DYLAN_NAME = "Dylan"
DYLAN_EMAIL = "dylan@systra.com"
DYLAN_PASSWORD = "Dylan2026!"

# Supprimer l'ancien compte Dylan s'il existe
cursor.execute("SELECT id FROM user WHERE email = ?", (DYLAN_EMAIL,))
existing = cursor.fetchone()
if existing:
    old_id = existing[0]
    cursor.execute("DELETE FROM user_projects WHERE user_id = ?", (old_id,))
    cursor.execute("DELETE FROM user WHERE id = ?", (old_id,))
    print(f"🗑️ Ancien compte Dylan supprimé (ID={old_id})")

# Créer Dylan avec bcrypt
hashed_password = bcrypt.generate_password_hash(DYLAN_PASSWORD).decode('utf-8')
cursor.execute("INSERT INTO user (name, email, password) VALUES (?, ?, ?)", 
               (DYLAN_NAME, DYLAN_EMAIL, hashed_password))
dylan_id = cursor.lastrowid
print(f"✅ Nouvel utilisateur créé: ID={dylan_id}")

print(f"\n👤 Identifiants de Dylan:")
print(f"   📧 Email: {DYLAN_EMAIL}")
print(f"   🔑 Mot de passe: {DYLAN_PASSWORD}")

# Tous les projets
cursor.execute('SELECT id, name FROM project')
projects = cursor.fetchall()
print(f"\n📁 {len(projects)} projet(s) trouvé(s):")
for p in projects:
    print(f"   - ID {p[0]}: {p[1]}")

# Ajouter Dylan à tous les projets
added = 0
for project_id, project_name in projects:
    cursor.execute('SELECT 1 FROM user_projects WHERE user_id = ? AND project_id = ?', (dylan_id, project_id))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO user_projects (user_id, project_id) VALUES (?, ?)', (dylan_id, project_id))
        print(f"   ➕ Dylan ajouté au projet: {project_name}")
        added += 1
    else:
        print(f"   ✓ Dylan a déjà accès au projet: {project_name}")

conn.commit()
conn.close()

print(f"\n🎉 Terminé! Dylan a maintenant accès à tous les projets ({added} nouveau(x)).")
