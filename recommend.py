from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
from numpy import dot
from numpy.linalg import norm

# 크롤링 데이터 전처리
data = pd.read_csv('패딩(musinsa).csv', encoding='cp949')

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
    score = cos_sim_score[1:21]
    tag_indices = [i[0] for i in score]

    return tag_indices


tfidf_gen = TfidfVectorizer()
data_tit = tfidf(data, tfidf_gen)

_input = input("관심있는 패딩 : ")
find_row = data[data['title'].str.contains(_input)]
print(find_row[['title', 'price']])
print()

_input = input("유사한 옷을 보고 싶으면 번호를, 아니면 NO를 : ")
if (_input == 'NO'):
    exit()
tit_20_q = data.iloc[topShow(data_tit, int(_input))]
print(str(_input), "번 옷과 유사한 옷들\n", tit_20_q[['title', 'price']])
tit_20_q.to_csv('result.csv', encoding='cp949', index=False)