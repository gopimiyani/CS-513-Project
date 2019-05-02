# https://www.datacamp.com/community/tutorials/k-means-clustering-python

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


df = pd.read_csv('./Final_Refined_Encoded_Normalysed.csv')

train, test = train_test_split(df, test_size = 0.3, random_state = 10)

print("***** Train_Set *****")
print(train.head())
print("\n")
print("***** Test_Set *****")
print(test.head())

print("***** Train_Set *****")
print(train.describe())
print("\n")
print("***** Test_Set *****")
print(test.describe())

print(train.columns.values)

print(train.isna().head())
print(test.isna().head())

print("*****In the train set*****")
print(train.isna().sum())
print("\n")
print("*****In the test set*****")
print(test.isna().sum())

print(train[['GPU', 'Price']].groupby(['GPU'], as_index=False).mean().sort_values(by='Price', ascending=False))
g = sns.FacetGrid(train, col='Price')
g.map(plt.hist, 'GPU', bins=20)

train.info()
test.info()

X = np.array(train.drop(['Price'], 1).astype(float))
y = np.array(train['Price'])
train.info()

# kmeans = KMeans(n_clusters
# =2) # You want cluster the passenger records into 2: Survived or Not survived
# kmeans = KMeans(n_clusters=3, max_iter=600, algorithm = 'auto')

kmeans = KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=600,
    n_clusters=5, n_init=10, n_jobs=1, precompute_distances='auto',
    random_state=None, tol=0.0001, verbose=0)

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
kmeans.fit(X)

# KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=300,
#     n_clusters=2, n_init=10, n_jobs=1, precompute_distances='auto',
#     random_state=None, tol=0.0001, verbose=0)

# kmeans = KMeans(algorithm='auto', copy_x=True, init='k-means++', max_iter=600,
#     n_clusters=5, n_init=10, n_jobs=1, precompute_distances='auto',
#     random_state=None, tol=0.0001, verbose=0)

correct = 0
for i in range(len(X)):
    predict_me = np.array(X[i].astype(float))
    predict_me = predict_me.reshape(-1, len(predict_me))
    prediction = kmeans.predict(predict_me)
    if prediction[0] == y[i]:
        correct += 1

print(correct/len(X))

# plt.show()