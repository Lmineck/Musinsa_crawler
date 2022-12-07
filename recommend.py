from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from numpy import dot
from numpy.linalg import norm

# 크롤링 데이터 전처리
data = pd.read_csv('패딩(musinsa).csv', encoding='cp949')
specialChars = '_!#$%^&*()[]'
for specialChar in specialChars:
    data['title'] = data['title'].str.replace(specialChar, '', regex=True)
data = data.drop_duplicates(subset='url')
data.to_csv('패딩(musinsa)_updated.csv', encoding='cp949', index=False)


# TF-IDF
def cos_sim(a, b):
    return dot(a, b) / (norm(a) * norm(b))


def tfidf(dataFrame, TfidfVectorizer):
    _tfidf = TfidfVectorizer.fit_transform(dataFrame['title'])

    return _tfidf


def topShow(data, num):
    cos_sim = linear_kernel(data, data)
    cos_sim_score = list(enumerate(cos_sim[num]))
    cos_sim_score = sorted(cos_sim_score, key=lambda x: x[1], reverse=True)
    score = cos_sim_score[1:11]
    tag_indices = [i[0] for i in score]

    return tag_indices


tfidf_gen = TfidfVectorizer()

data_tit = tfidf(data, tfidf_gen)

for i in range(len(data)):
    print(i, '/', len(data))
    tit_10_q = data['title'].iloc[topShow(data_tit, i)]
    print(str(i), "번 옷과 유사한 옷들\n", tit_10_q)
