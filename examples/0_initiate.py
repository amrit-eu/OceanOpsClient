from OceanOpsClient import OceanOpsClient

client = OceanOpsClient.from_env()
print(client.settings)

