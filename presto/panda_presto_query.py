# -*- coding:UTF-8 -*-


import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine

"""
报错：sqlalchemy.exc.NoSuchModuleError: Can‘t load plugin: sqlalchemy.dialects:presto

该报错需要安装pyhive
pip install pyhive
"""

#  presto://user:passw@hostname:port/db
#  connect_args={'auth':LDAP, 'protocol': 'https', 'session_props': {'query_max_run_time': '1234m'}}
engine = create_engine("presto://hive@x.x.x.x:8889/hive")

df = pd.read_sql("SELECT country as country, province as province FROM amber_tableau.vw_app_login limit 1", engine)
# print(df.columns, df.values)
for idx, data in df.iterrows():
    print("[{}]: {}".format(idx, data))

print("=============================\n")

for colName, data in df.items():
    print("colName:[{}]\ndata:{}".format(colName, data))

df.plot(kind="bar", x="country", y="province")
plt.show()
