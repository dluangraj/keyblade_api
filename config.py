import os

basedir = os.path.abspath(os.path.dirname(__file__))

# give access to the project in any OS we find ourselves in
# allow outside files/folders to be added to the project from
# base directory

class Config():
    """
    Set Config variables for the Flask app.
    Using Environment variables where available otherwise
    Create the config variable if not done already.
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or "You will never guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or 'sqlife:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False