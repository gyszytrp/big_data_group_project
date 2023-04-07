# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 23:47:07 2023
@author: Luna
"""
# pip install pyspark
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import lit, col,isnan
from pyspark.ml.recommendation import ALSModel


class cf_recommend:

    def __init__(self, dataroute):
        """# 1. Read three tables and model"""


        # Remember to change the dataroute below to where you store data and model. The data are too large which can not be uploaded to github.
        self.dataroute=dataroute


        self.bgg_ratings_with_avg_schema = StructType([
            StructField("Name", StringType(), True),
            StructField("BGGId", IntegerType(), True),
            StructField("avg_rating", DoubleType(), True),
            StructField("count_rating", IntegerType(), True),
        ])

        self.rating_df_schema = StructType([
            StructField("BGGId", IntegerType(), True),
            StructField("Rating", DoubleType(), True),
            StructField("UserId", IntegerType(), True),
        ])

        self.bgg_df_schema = StructType([
            StructField('BGGId', IntegerType()),
            StructField('Name', StringType()),
        ])




        # Initialize spark session
        self.spark = SparkSession.builder.appName("Recommendation_system").getOrCreate()

        # Load data and model

        self.bgg_ratings_400 = self.spark.read.format("csv").option("header", "true").schema(self.bgg_ratings_with_avg_schema).load("./data/bgg_ratings_400.csv")
        self.df_rating = self.spark.read.format("csv").option("header", "true").schema(self.rating_df_schema).load("./data/user_ratings.csv")
        self.df_bgg = self.spark.read.format("csv").option("header", "true").schema(self.bgg_df_schema).load("./data/Games_Feture_Engineering.csv")

        self.bgg_model = ALSModel.load("./data/CF-Model")


        """# 2. Define recommendation function"""

    def recommend(self,user_id, top_n):
        # Get rated BGGIds for the user
        rated_bgg_ids = self.df_rating[self.df_rating['UserId'] == user_id].select('BGGId')

        # Filter out the games that the user has already rated
        not_rated_df = self.df_bgg.join(rated_bgg_ids, self.df_bgg['BGGId'] == rated_bgg_ids['BGGId'], 'left_anti')

        # Add a column with the user_id as "userId".
        my_unrated_bgg_df = not_rated_df.withColumn('UserId', lit(user_id))

        # Predict ratings for the games that the user has not rated yet.
        raw_predicted_ratings_df = self.bgg_model.transform(my_unrated_bgg_df)

        # Filter out NaN predictions
        predicted_ratings_df = raw_predicted_ratings_df.filter(~ isnan(col('prediction')))

        # Filter out games if count < 400
        predicted_ratings_df2 = predicted_ratings_df.withColumnRenamed("BGGId", "p_BGGId").withColumnRenamed("Name", "p_Name")
        predicted_highest_rated_games_df = predicted_ratings_df2.join(self.bgg_ratings_400, predicted_ratings_df2.p_BGGId == self.bgg_ratings_400.BGGId).\
            sort('prediction',ascending = False)

        # Get recommendation
        rec = predicted_highest_rated_games_df.select("UserId", "p_BGGId", "p_Name", "prediction", "count_rating",
                                                    "avg_rating").head(top_n)
        rec = pd.DataFrame(rec, columns=["UserId", "p_BGGId", "p_Name", "prediction", "count_rating", "avg_rating"])

        # Return the Top N results
        return rec






