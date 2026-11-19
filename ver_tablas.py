from app import app, db

with app.app_context():
    print("Tablas en la base de datos:", db.metadata.tables.keys())