import json
from config import Settings
from urllib.request import urlopen

PASSPORT_TEMPLATE = ("https://www.ocean-ops.org/passports/examples/"
                     "a-input-passport.json")


class OceanOps:
    def __init__(self, settings: Settings):

        self.BASE_URL = "https://www.ocean-ops.org/api/data"
        self.GET_ID_URL = f"{self.BASE_URL}/platforms/getid"

        self._settings = settings
        self._headers = {
            "Content-Type": "application/json",
            "X-OceanOPS-Metadata-ID": settings.API_KEY_ID,
            "X-OceanOPS-Metadata-Token": settings.API_KEY_TOKEN
        }
        self._load_passport_template()

    def _load_passport_template(
            self,
            template_file=PASSPORT_TEMPLATE
    ):
        path = template_file

        try:
            if path.startswith(("http://", "https://")):
                with urlopen(path) as response:
                    self._passport_template = json.load(response)
            else:
                with open(path, "r", encoding="utf-8") as f:
                    self._passport_template = json.load(f)

        except Exception as e:
            raise RuntimeError(
                f"Failed to load passport template '{path}'"
            ) from e

    def test_passport(self, candidate, standard=None, path=""):

        if standard is None:
            standard = self._passport_template

        # Type mismatch
        if not isinstance(candidate, type(standard)):
            raise TypeError(
                f"Type mismatch at '{path}': expected "
                f"{type(standard).__name__}, got {type(candidate).__name__}"
            )

        # Dict validation
        if isinstance(standard, dict):
            for key, value in candidate.items():
                if key not in standard:
                    raise KeyError(
                        f"Unexpected key '{path + '.' + key if path else key}'")

                self.test_passport(
                    standard[key],
                    value,
                    path + "." + key if path else key
                )

        # List validation
        elif isinstance(standard, list):
            if len(standard) == 0:
                return  # cannot infer element type

            standard_item = standard[0]
            for i, item in enumerate(candidate):
                self.test_passport(
                    standard_item,
                    item,
                    f"{path}[{i}]"
                )
        else:
            pass

        return True

    def get_wigos_id(self, ):
        pass

    def push_passport(self):
        # test_result = self.test_passport(candidate="None", standard="None")
        # print(test_result)
        pass


if __name__ == "__main__":
    settings = Settings()
    ops = OceanOps(settings=settings)
    with open("templates/thornton_passport.json", "r", encoding="utf-8") as f:
        candidate_passport = json.load(f)
    ops.test_passport(candidate_passport)


