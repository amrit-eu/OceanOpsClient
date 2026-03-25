import json
import requests
from typing import Any
from typing import Dict
from typing import Union
from typing import Optional
from pathlib import Path
from jsonschema import validate
from OceanOpsClient.config import Settings


class OceanOps:
    BASE_URL = "https://www.ocean-ops.org/api/data"
    DEFAULT_SCHEMA_URL = "https://www.ocean-ops.org/passports/examples/a-passport-input.schema.json"
    LOCAL_SCHEMA_PATH = Path(__file__).parent / "passport_schema" / "local_schema.json"

    def __init__(self, settings: Optional["Settings"] = None):
        self.settings = settings

        # Build headers only if credentials exist
        if self.settings:
            self.headers = {
                "Content-Type": "application/json",
                "X-OceanOPS-Metadata-ID": self.settings.API_KEY_ID,
                "X-OceanOPS-Metadata-Token": self.settings.API_KEY_TOKEN.get_secret_value(),
            }
        else:
            self.headers = None  # read-only mode

    @classmethod
    def from_env(cls, env_file: str | None = None):
        try:
            settings = Settings(_env_file=env_file) if env_file else Settings()
            return cls(settings)
        except Exception:
            # Failed to load credentials → return read-only client
            return cls(None)

    @classmethod
    def from_credentials(cls, key_id: str, token: str):
        settings = Settings(API_KEY_ID=key_id, API_KEY_TOKEN=token)
        return cls(settings)

    # Example method for read-only access
    def get_platform(self, ptfWigosId: str) -> Dict[str, Any]:
        if not ptfWigosId:
            raise ValueError("ptfWigosId must be provided")

        url = f"{self.BASE_URL}/platform/wigosid/{ptfWigosId}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    # Example method for push
    def push_data(self, payload: dict):
        """
        Push data. Requires credentials.
        """
        if not self.headers:
            raise RuntimeError("Cannot push data: credentials required")
        # ... call API with self.headers
        return {"status": "success"}

    def validate_passport_json(
            self,
            local_json: Union[str, dict],
            use_local_schema: bool = False,
    ) -> bool:

        if use_local_schema:
            schema_path = self.LOCAL_SCHEMA_PATH

            if not schema_path.exists():
                raise FileNotFoundError(
                    f"Local schema not found: {schema_path}")

            print(f"Using LOCAL schema: {schema_path}")

            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)

        else:
            print("Using ONLINE OceanOPS schema")

            resp = requests.get(self.DEFAULT_SCHEMA_URL)
            resp.raise_for_status()
            schema = resp.json()

        # --- Load data ---
        if isinstance(local_json, (str, Path)):
            with open(local_json, "r", encoding="utf-8") as f:
                data = json.load(f)
        elif isinstance(local_json, dict):
            data = local_json
        else:
            raise ValueError("local_json must be a file path or a dictionary")

        # --- Validate ---
        validate(instance=data, schema=schema)

        print("JSON is valid against the schema")
        return True


