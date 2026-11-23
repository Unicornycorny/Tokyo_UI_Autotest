from pathlib import Path
from typing import Self

from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class TestData(BaseModel):
    category: str
    subcategory: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter=".",
        extra="ignore",
    )

    app_url: HttpUrl
    headless: bool = False
    browser: str = "chrome"
    videos_dir: Path = Path("./videos")
    tracing_dir: Path = Path("./tracing")
    test_data: TestData

    @classmethod
    def initialize(cls) -> Self:
        settings = cls()
        settings.videos_dir.mkdir(exist_ok=True)
        settings.tracing_dir.mkdir(exist_ok=True)
        return settings

    def get_base_url(self) -> str:
        return str(self.app_url)


settings = Settings.initialize()
