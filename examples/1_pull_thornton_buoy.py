from pprint import pprint
from OceanOpsClient import OceanOpsClient

wigosID = "0-22000-0-6204817"
client = OceanOpsClient()
resp = client.get_platform(ptfWigosId=wigosID)
pprint(resp)
