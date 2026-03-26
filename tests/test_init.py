import sys
import os
import OceanOpsClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_import_and_version():
    print("OceanOpsClient version:", OceanOpsClient.__version__)
    client = OceanOpsClient.OceanOpsClient()
    print("Client loaded:", client)


if __name__ == "__main__":
    test_import_and_version()

