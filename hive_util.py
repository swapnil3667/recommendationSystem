import hive_utils

query = """
    SELECT *
    FROM user_attributes limit 1
"""
hive_client = hive_utils.HiveClient(
    server='localhost',
    port='9083',
    db='viki',
)
for row in hive_client.execute(query):
    print row
