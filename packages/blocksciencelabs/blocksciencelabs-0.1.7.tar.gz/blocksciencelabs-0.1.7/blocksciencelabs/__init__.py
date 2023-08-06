import client
import common

import pandas as pd
import functools, pickle, operator

def fetch_results(jobs: list, conn):
  job_ids = f"{jobs}"[1:-1]
  sql_query = f"SELECT * FROM job_result WHERE job_id IN ({job_ids});"
  df = pd.read_sql_query(sql_query, conn)
  ser_results = df['data'] \
      .transform(lambda x:  pickle.loads(bytes.fromhex(x))) \
      .to_list()
  results = pd.DataFrame(functools.reduce(operator.iconcat, ser_results, []))
  return results