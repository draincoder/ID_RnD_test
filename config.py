import configparser
from dataclasses import dataclass


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: int
    use_redis: bool
    skip_updates: bool


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot.get("token"),
            admin_ids=[int(admin_id) for admin_id in tg_bot.get("admin_ids").split(',')],
            use_redis=tg_bot.getboolean("use_redis"),
            skip_updates=tg_bot.getboolean("skip_updates"),
        ),
        db=DbConfig(**config["db"]),
    )
