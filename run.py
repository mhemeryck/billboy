import sys
from app import app, db

def main():
    db.create_all()
    app.run()

if __name__ == '__main__':
    sys.exit(main())
