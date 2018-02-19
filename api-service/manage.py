from flask_script import Manager

from api import app, db


manager = Manager(app)

@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == '__main__':
    manager.run()


# import os, sys
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__name__), ',' )))

# from flask_script import Manager, Server
# from application import creat_app

# app = creat_app()

# manager = Manager(app)

# manager.add_command("runserver", Server(
#     use_debugger = True,
#     use_reloader = True,
#     host = os.getenv('IP', '0.0.0.0'),
#     port = int(os.getenv('PORT', 5000)))
# )
# if __name__ == "__main__":
#     manager.run()
