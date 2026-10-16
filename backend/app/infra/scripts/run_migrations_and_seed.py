import asyncio

from app.infra.scripts.run_migrations import run_migrations
from app.infra.scripts.seed_data import seed_data


def main() -> None:
    run_migrations()
    asyncio.run(seed_data())
    print("Migrations and seed completed successfully")


if __name__ == "__main__":
    main()