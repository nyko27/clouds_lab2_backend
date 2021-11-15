from setup import create_app, db
from cfg.config import GcpConfig

flask_app = create_app(config_cls=GcpConfig)


def drop_db():
    with flask_app.app_context():
        db.drop_all()


def init_db():
    with flask_app.app_context():
        db.create_all()


def run():
    init_db()
    flask_app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    run()

