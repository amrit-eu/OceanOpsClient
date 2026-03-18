from pprint import pprint
from pydantic_settings import BaseSettings
from pydantic_settings import CliSettingsSource
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    API_KEY_ID: str
    API_KEY_TOKEN: str

    model_config = SettingsConfigDict(
        env_file=".env"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            CliSettingsSource(settings_cls),  # CLI first
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )


if __name__ == "__main__":
    settings = Settings()
    pprint(settings)
