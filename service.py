from supports.s3_support  import S3Support
from supports.service_support import ServiceSupport
s3_support = S3Support()

class Service:

    def __init__(self):
        self.df_ratings = s3_support.load_ratings()
        self.df_movies  = s3_support.load_movies()
        self.model      = s3_support.load_knn_model()



    def recommender_movies(self,movie_id,n_results = 5):
        n_results += 1
        response = {'source':{},'recommerders':[]}

        print('Creating Matrix......')
        df_matrix = ServiceSupport.create_matrix(self.df_ratings)
        print('Matrix created')
   
        distances,indices = ServiceSupport.calculate_distance_index(self.model,df_matrix,n_results,movie_id)
     
        for i in range(0,len(distances.flatten())):
            if i == 0:
            
                movie = self.df_movies[self.df_movies['movieId']==movie_id]
                print(movie)
                response['source'] = {
                    "id": str(movie['movieId'].values[0]),
                    "title": str(movie['title'].values[0]).strip(),
                    "genres": movie['genres'].values[0],
                    "year" : movie['year'].values[0]
                }
        
            else:
                idx = df_matrix.index[indices.flatten()[i]]
                
                movie = self.df_movies[self.df_movies['movieId']==idx]
                
                movie_dist = distances.flatten()[i] *100

                response['recommerders'].append({
                    "id": str(movie['movieId'].values[0]),
                    "position": str(i),
                    "title": str(movie['title'].values[0]).strip(),
                    "genres": movie['genres'].values[0],
                    "year": movie['year'].values[0],
                    "distance": movie_dist
                })
                
                

        return response