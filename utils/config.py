from dataclasses import dataclass
from environs import Env


@dataclass
class SupabaseConfig:
    url: str
    key: str


@dataclass
class Config:
    supabase: SupabaseConfig


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        supabase=SupabaseConfig(
            url=env.str("SUPABASE_URL"),
            key=env.str("SUPABASE_KEY")
        ),
    )

