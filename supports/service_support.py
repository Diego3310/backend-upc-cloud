
import pandas as pd

class ServiceSupport: 

    @staticmethod
    def create_matrix(df_ratings):
        df_matrix = pd.pivot_table(df_ratings,index='userId',columns='movieId',values='rating').fillna(0)
        df_matrix = df_matrix.T
        return df_matrix
    
    @staticmethod
    def calculate_distance_index(model,df_matrix,n_results,movie_id):
        query_index= df_matrix.index.get_loc(movie_id)
        query_vector = df_matrix.iloc[query_index].values.reshape(1,-1)
        distances, indices = model.kneighbors(query_vector,n_neighbors=n_results)
        return distances,indices