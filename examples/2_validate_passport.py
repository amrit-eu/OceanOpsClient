from OceanOpsClient import OceanOpsClient

client = OceanOpsClient()
passport = "passport_thornton_buoy.json"
status = client.validate_passport_json(passport)

print(status)
