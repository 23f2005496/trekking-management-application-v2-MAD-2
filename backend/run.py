from app import db, create_app, login_manager
from config.commands import register_commands
from app.models.user import User

# API Blueprints

from app.api.auth_api import auth_api
from app.api.admin_api import admin_api
from app.api.staff_api import staff_api
from app.api.trekker_api import trekker_api

app = create_app()


app.register_blueprint(auth_api, url_prefix="/api")
app.register_blueprint(admin_api, url_prefix="/api/admin")
app.register_blueprint(staff_api, url_prefix="/api/staff")
app.register_blueprint(trekker_api, url_prefix="/api/trekker")


register_commands(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)



if __name__ == "__main__":
    app.run(debug=True)
