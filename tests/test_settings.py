import unittest
from pathlib import Path
from unittest import mock
from OceanOpsClient import OceanOpsClient


class TestOceanOps(unittest.TestCase):
    def setUp(self):
        # Environment values we'll inject in tests
        self.env = {
            "API_KEY_ID": "fake-id",
            "API_KEY_TOKEN": "fake-token",
        }

    def test_from_env(self):
        # Inject environment variables so the real Settings() picks them up
        with mock.patch.dict("os.environ", self.env, clear=False):
            client = OceanOpsClient.from_env()
            self.assertEqual(client.settings.API_KEY_ID, "fake-id")
            # API_KEY_TOKEN is a SecretStr when using real Settings
            self.assertEqual(client.settings.API_KEY_TOKEN.get_secret_value(), "fake-token")

    def test_from_cli(self):
        # Also exercise creating a client when env vars are present
        env_path = Path(__file__).parent / ".env"
        with mock.patch.dict("os.environ", self.env, clear=False):
            client = OceanOpsClient.from_env()
            self.assertEqual(client.settings.API_KEY_ID, "fake-id")
            self.assertEqual(client.settings.API_KEY_TOKEN.get_secret_value(), "fake-token")

    def test_init_without_settings(self):
        client = OceanOpsClient()
        self.assertIsNone(client.settings)


