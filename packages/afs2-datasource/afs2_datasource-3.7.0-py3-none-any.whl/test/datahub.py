import os

# os.environ['PAI_DATA_DIR'] = 'eyJ0eXBlIjoiZGF0YWh1Yi1maXJlaG9zZSIsImRhdGEiOnsiY3JlZGVudGlhbCI6eyJ1cmkiOiJpbmZsdXhkYjovLzpAMTcyLjE2LjguNDA6ODA4Ni9kYXRhaHViIiwidXNlcm5hbWUiOiJ1c2VybmFtZSIsInBhc3N3b3JkIjoicGFzc3dvcmQiLCJob3N0IjoiODA4NiIsImRhdGFiYXNlIjoiaW5mbHV4ZGI6Ly86QDE3Mi4xNi44LjQwOjgwODYvZGF0YWh1YiJ9LCJkYXRhaHViX2NvbmZpZyI6W3sibmFtZSI6ImRhdGFodWItMSIsInByb2plY3RfaWQiOiI0a3ZMSHdhOXdVd28iLCJub2RlX2lkIjoiODVhYmI5MjMtMTJiMi00Y2I5LWI4YmUtZTU4NDczNTQ3M2Q1IiwiZGV2aWNlX2lkIjoiRGV2aWNlSURfMCIsInRhZ3MiOlt7Im5hbWUiOiJUYWdOYW1lX2FuYV8wIn1dfV0sImRhdGFodWJfdXJsIjoiaHR0cDovL3BvcnRhbC1kYXRhaHViLWRhdGFodWItZWtzMDA4LnNhLndpc2UtcGFhcy5jb20iLCJkYXRhaHViQXV0aCI6IlkyTXVlV0Z1WjBCaFpIWmhiblJsWTJndVkyOXRMblIzT21OallUaGpZV0V6UUZOek1BPT0iLCJ1c2VybmFtZSI6ImNjLnlhbmdAYWR2YW50ZWNoLmNvbS50dyIsInRpbWVMYXN0Ijp7Imxhc3REYXlzIjoxLCJsYXN0SG91cnMiOjAsImxhc3RNaW5zIjowfX19'


# from afs2datasource import DBManager, constant

# manager = DBManager()
# manager.connect()
# data = manager.execute_query()
# print(data)

from afs2datasource import DBManager, constant
manager = DBManager(db_type=constant.DB_TYPE['DATAHUB'],
  username='ssopassroot@email.com',  # sso username
  password='ToorSs@p0SS',  # sso password
  datahub_url='https://portal-datahub-ensaas.aifs.wise-paas.com',
  datahub_config=[{
    "name": "test0510", # dataset name
    "project_id": "afs-demo",#datahub的mongodb数据库中不会存这个参数
    "node_id": "90b016ce-d171-423b-b16f-2d2eeb82f49e",
    "device_id": "Device1",
    "tags": [
      "ATag0"
    ]
  }],
  uri='influxdb://d44b1476-f532-4ce2-8244-fec7bffd858e:0ERVNiAbxCBWJZldFT6JMHdr4@172.17.21.111:8086/1f65d529-898c-46d8-8d71-30671a3f820b',
  # timeRange or timeLast
  #timeRange=[{'start': start_ts, 'end': end_ts}],
  timeLast={'lastDays': 360, 'lastHours': 77, 'lastMins': 77}
)
manager.connect()
df = manager.execute_query()
print(df)