import sys

from app import app, db, init_users


def main():
    db.create_all()
    init_users()
    app.run()

if __name__ == '__main__':
    sys.exit(main())
