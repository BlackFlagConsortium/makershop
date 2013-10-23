from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy(
    session_options={
        'autoflush': True,
        'expire_on_commit': False,
    }
)