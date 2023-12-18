from app.db import engine
from app.models import Project, Task, User
from starlette_admin.contrib.sqla import Admin
from starlette_admin.contrib.sqla import ModelView as BaseModelView


class ModelView(BaseModelView):
    exclude_fields_from_create = ["created_at", "updated_at"]
    exclude_fields_from_edit = ["created_at", "updated_at"]


def init_admin(app):
    admin = Admin(engine, templates_dir="templates/admin")
    admin.add_view(ModelView(User))
    admin.add_view(ModelView(Project))
    admin.add_view(ModelView(Task))
    admin.mount_to(app)
