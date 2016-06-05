import numpy as np
import itertools
np.set_printoptions(precision=9)
import math
import timeit
import gzip
import pandas as pd
from sqlalchemy import create_engine


# select product, ratings, average rating from table where number of reviews >= 1000 GroupBy productID

# I will select 5 or 10 ratings at random from the test products to use as predictors for the average rating
# check the scikit-learn tutorial for how to predict a continuous variable

def parse(path):
  g = gzip.open(path, 'rb')
  for l in g:
    yield eval(l)


def Load_Review_Chunk(path, destination, chunksize):
  start_time = timeit.default_timer()
  dfDict = {}
  i = 22645001
  chunk = 4530
  for d in parse(path):
      dfDict[i] = d
      i += 1
      if i > chunksize * chunk:
        chunk_to_SQL(dfDict, destination)
        print("Chunk #", chunk, " saved. Time elapsed: ", int(timeit.default_timer() - start_time), " seconds", end='\r')
        dfDict = {}
        chunk += 1
  chunk_to_SQL(dfDict, destination)
  print("Last Chunk #", chunk, "Total time elapsed: ", int(timeit.default_timer() - start_time), " seconds", end='\r')
  return


def chunk_to_SQL(dfDict, destination):
  df = pd.DataFrame.from_dict(dfDict, orient='index')
  # I can use reviewTime or unixReviewTime to select first 10 reviews to train on
  # maybe I'll keep reviewerID so I can rematch with reviewText if I want to
  df.drop(['helpful', 'reviewText', 'reviewerName', 'summary', 'reviewTime'], axis=1, inplace = True)
  #print(df.head())
  #print(df.head())
  df.to_sql('reviews', disk_engine, if_exists='append', index_label = 'index')
  return

def step1():
  Load_Review_Chunk(path, destination, 5000)
  print(df.head())
  print("Review Chunk #", chunk, "chunk size", df.size)
  print("total size", df.size)
  # group by asin
  # select asin where asin rows >= 1000
  grouped = df.groupby(['asin']).filter(lambda x: len(x)>=1000)
  print("grouped size", grouped.size)
  
  sql = "SELECT * FROM reviews LIMIT 5 OFFSET (SELECT COUNT(*) FROM reviews)-5"
  df = pd.read_sql_query(sql, disk_engine, index_col = 'index')
  print(df.head())

  # what I want seems too complex, so breaking it down.. means as separate table, then join

  # would be better to combine this query with the next one rather than creating a subset table, so I don't have to redo after finishing populating database
  # for now, it gives me something to practice on
  return


def step2():
  df = pd.DataFrame
  # make list of unique asin
  sql = "SELECT DISTINCT asin FROM subset"
  asinList = pd.read_sql_query(sql, disk_engine)
  print(asinList.head())
  print(len(asinList.index))
  for row in asinList['asin'].tolist():
    print("loading: ", row)
    sql = "SELECT * FROM subset WHERE asin = '" + row + "' LIMIT 20"
    temp_df = pd.read_sql_query(sql, disk_engine, index_col = 'index')
    print("Temp df:\n", temp_df.head())
    if len(temp_df.index)>1:
      print("appending temp_df to df")
      if df.empty:
        df = temp_df
      else:
        df = df.append(temp_df, ignore_index=True)
    
  print(df.head(), df.tail())
  sql = "CREATE TABLE subset AS SELECT * FROM reviews WHERE asin IN ( SELECT asin FROM reviews GROUP BY asin HAVING COUNT (asin)>999)"
  disk_engine.execute(sql)
  print("new table created")
  sql = "SELECT * FROM subset a WHERE a.'index' IN ( SELECT b.'index' FROM subset b WHERE b.'index' IS NOT NULL AND a.'asin' = b.'asin' ORDER BY b.'unixReviewTime', b.'index' LIMIT 20) ORDER BY a.'asin', a.'unixReviewTime'" 

  # df = pd.read_sql_query(sql, disk_engine, index_col = 'index')
  # print(df.head())
  
  #df.to_sql('means', disk_engine, if_exists='replace', index_label = 'index')
  df.to_csv(text_destination)
  print("Success! Hooray!")
  return


def step3(text_source, text_destination):
  # find average overall from data for each asin, and load to df1
  sql = "SELECT asin, avg(overall) FROM subset GROUP BY asin"
  df1 =  pd.read_sql_query(sql, disk_engine)

  # load the ratings into df2
  df2 = pd.read_csv(text_source)

  # join on asin, keeping just df2 (left)
  df = pd.merge(df2, df1, on='asin', how='left')

  # resave
  print(df.head(), df.tail())
  df.to_csv(text_destination)
  print("Step 3 Successful! Hooray!")
  return

def step4(text_source, text_destination):
  # find average of just first 20 ratings
  df = pd.read_csv(text_source)
  df['avg20'] = df['overall'].groupby(df['asin']).transform(np.mean)
  # save as new file
  print(df.head(), df.tail())
  df.to_csv(text_destination)
  print("step 4 successful!")
  return

def step5(text_source):
  # scatterplot with trend line, x=avg20, y=avg(overall)
  df = pd.read_csv(text_source)
  df.plot(kind='scatter', x='avg20', y='avg(overall)')
  return

def step6():
  # reviewerMean - mean helpfulness of a reviewers reviews

  return

def main():
  path = '/Volumes/Storage/Lab data/Data Analysis/metadata.json.gz'
  database = '/Volumes/STORAGECARD/ratingsForReviewsOver1000.db'
  text_source = '/Volumes/STORAGECARD/ratingsAverage.csv'
  text_destination = '/Volumes/STORAGECARD/ratingsAverage.csv'

  global disk_engine
  disk_engine = create_engine('sqlite:///' + database)
  
  #step1()

  #step2()

  #step3(text_source, text_destination)

  #step4(text_source, text_destination)

  #step5(text_source)

  step6()

  return


if __name__ == '__main__':
   main()

