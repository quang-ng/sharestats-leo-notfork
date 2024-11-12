import os
from dataclasses import dataclass

@dataclass
class DatabaseConfig:
    host: str = os.getenv('DB_HOST', 'localhost')
    port: int = int(os.getenv('DB_PORT', '5432'))
    database: str = os.getenv('DB_NAME', 'postgres')
    user: str = os.getenv('DB_USER', 'postgres')
    password: str = os.getenv('DB_PASSWORD', '')

def get_database_url() -> str:
    config = DatabaseConfig()
    return f"postgresql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}" 