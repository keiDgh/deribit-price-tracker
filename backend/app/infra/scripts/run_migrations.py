from app.infra.settings.config import settings

from alembic import command
from alembic.config import Config

def run_migrations() -> None:
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", settings.database_url)
    command.upgrade(cfg, "head")