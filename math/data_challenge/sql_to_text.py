import pandas as pd
import gzip
from sqlalchemy import create_engine
import timeit

def main():
  start_time = timeit.default_timer()
  path = '/Volumes/Storage/Lab data/Data Analysis/'
  filename = 'sampledata.txt'
  destination = '/Volumes/Storage/Lab data/Data Analysis/electronicsreviews.db'
  disk_engine = create_engine('sqlite:///' + destination)
  
  sql = "SELECT * FROM electronics LIMIT 500000"
  df = pd.read_sql_query(sql, disk_engine, index_col = 'index')

  print("Length of datatable: ", len(df))
  print(df['reviewText'].head())
  series = pd.Series(df['reviewText'])
  series.to_csv((path + filename), sep='&', header=False, index=False)
  print("Time elapsed: ", int(timeit.default_timer() - start_time), " secs")
  
  return


if __name__ == '__main__':
   main()

