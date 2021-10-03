
import pandas as pd
from s3fs.core import S3FileSystem
s3client = S3FileSystem()
import numpy as np
import os;
import pickle
import boto3
s3Boto3 = boto3.resource('s3')

BUCKET_KEY_RATINGS  = os.getenv('BUCKET_KEY_RATINGS') 
BUCKET_KEY_MOVIES   = os.getenv('BUCKET_KEY_MOVIES')
BUCKET_KEY_MODEL    = os.getenv('BUCKET_KEY_MODEL')
BUCKET_NAME         = os.getenv('BUCKET_MOVIES')
FILE_MODEL_NAME     = '/tmp/' + BUCKET_KEY_MODEL.split('/')[1]

class S3Support:
    
   
    def load_movies(self):
        print('Loading Movies DataFrame....')
        movies = np.load(s3client.open('{}/{}'.format(BUCKET_NAME, BUCKET_KEY_MOVIES)),allow_pickle=True)
        movies = pd.DataFrame(movies, columns = ['movieId','title','genres','year'])
        print('Movies DataFrame Loaded')
        # Cast properties
        movies.movieId   = movies.movieId.astype(int)
        movies.title    = movies.title.astype(str)
        movies.genres   = movies.genres.astype(str)
        movies.year     = movies.year.astype(str)

        return movies

    def load_ratings(self): 
        print('Loading Rating DataFrame....')
        ratings = np.load(s3client.open('{}/{}'.format(BUCKET_NAME, BUCKET_KEY_RATINGS)),allow_pickle=True)
        ratings = pd.DataFrame(ratings, columns = ['userId','movieId','rating'])
        print('Rating DataFrame Loaded')
        # Cast properties
        ratings.userId  = ratings.userId.astype(int)
        ratings.movieId = ratings.movieId.astype(int)
        ratings.rating  = ratings.rating.astype(np.float32)
        return ratings

    def load_knn_model(self):
        
        model = None
        if not os.path.isfile(FILE_MODEL_NAME):
            print('Downloading ML Model from S3 Bucket.....')
            with open(FILE_MODEL_NAME, 'wb') as data:
                s3Boto3.Bucket(BUCKET_NAME).download_fileobj(BUCKET_KEY_MODEL, data)
            print('ML Model downloaded')
            print('Loading ML Model....')
            with open(FILE_MODEL_NAME, 'rb') as data:
                model = pickle.load(data)
            print('ML Model loaded')
        else:
            print('Loading ML Model....')
            with open(FILE_MODEL_NAME, 'rb') as data:
                model = pickle.load(data) 
            print('ML Model loaded')
        return model