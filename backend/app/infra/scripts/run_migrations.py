from alembic import command
from alembic.config import Config
from app.infra.settings.config import settings


def run_migrations() -> None:
    cfg = Config("alembic.ini")
    sync_url = f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    cfg.set_main_option("sqlalchemy.url", sync_url)
    command.upgrade(cfg, "head")