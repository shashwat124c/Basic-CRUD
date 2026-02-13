from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)


# run.py
#    ↓
# __init__.py loads
#    ↓
# create_app()
#    ↓
# db.init_app(app)
#    ↓
# routes imported
#    ↓
# models imported
#    ↓
# blueprint registered
#    ↓
# create tables
#    ↓
# server starts
#    ↓
# request comes
#    ↓
# route executes
#    ↓
# DB query runs
#    ↓
# template rendered
#    ↓
# response sent
