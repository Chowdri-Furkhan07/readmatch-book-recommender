import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# STEP 1: LOAD DATA
# IMPORTANT: your file is CSV even if named .xls
data = pd.read_csv("books.xls", engine='python')

# If columns are merged into one → fix
if len(data.columns) == 1:
    data = data[data.columns[0]].str.split(",", expand=True)

    data.columns = [
        'isbn13','isbn10','title','subtitle','authors','categories',
        'thumbnail','description','published_year',
        'average_rating','num_pages','ratings_count'
    ]


# STEP 2: CLEAN DATA
data.columns = data.columns.str.strip()

# Fill missing values
data['title'] = data['title'].fillna('')
data['authors'] = data['authors'].fillna('')
data['categories'] = data['categories'].fillna('')
data['description'] = data['description'].fillna('')
data['thumbnail'] = data['thumbnail'].fillna('')

# Remove duplicates
data.drop_duplicates(subset='title', inplace=True)


# STEP 3: CREATE TAGS
data['tags'] = (
    data['title'] + " " +
    data['authors'] + " " +
    data['categories'] + " " +
    data['description']
)

data['tags'] = data['tags'].apply(lambda x: x.lower())


# STEP 4: VECTORIZATION
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(data['tags']).toarray()


# STEP 5: SIMILARITY
similarity = cosine_similarity(vectors)

# STEP 6: SAVE FILES
pickle.dump(data, open('books.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("Training completed successfully!")