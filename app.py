from flask import Flask,request
import flask
import pandas as pd 
from flask_table import Table, Col
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
class Results(Table):
    id = Col('Id', show=False)
    title = Col('')
# features = ['keywords','cast','genres','director']
# for feature in features:
# 	df[feature] = df[feature].fillna('')

def get_title_from_index(index):
	return df2[df2.index == index]["title"].values[0]

def get_index_from_title(title):
	return df2[df2.title == title]["index"].values[0]

df2 = pd.read_csv('./tmdb.csv')
data = df2['original_title'].values.tolist()

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['soup'])

df2 = df2.reset_index()

def get_recommendations(title):
	cosine_sim = cosine_similarity(count_matrix) 
	#movie_user_likes = ["Avatar","Titanic","The Beach"]
	movie_index,similar_movies = [],[]
	sorted_similar_movies,result = [],[]
	j = 0
	for i in range(1):
		# print(title[i])
		movie_index.append(get_index_from_title(title[i]))
		similar_movies.append(list(enumerate(cosine_sim[movie_index[i]])))
		sorted_similar_movies = sorted(similar_movies[i],key=lambda x:x[1],reverse=True)
		#print(sorted_similar_movies)
		for element in sorted_similar_movies[1:]:
			result.append(get_title_from_index(element[0]))
			j = j+1
			if j>4:
				break
	return result

@app.route('/', methods=['GET', 'POST'])
def index():
	if flask.request.method == 'GET':
		return(flask.render_template('home.html',data = data,recommended_movie  = ''))
	if flask.request.method == 'POST':
		m_name = request.form.getlist('browser')
		result_final = get_recommendations(m_name)
		table = Results(result_final)
		#table.border = True

		return flask.render_template('home.html',data = data,recommended_movie  = table)

if __name__ == '__main__':
	app.run(debug=True)