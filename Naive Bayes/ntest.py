# Required Python Machine learning Packages
import pandas as pd
import numpy as np
# For preprocessing the data
from sklearn.preprocessing import Imputer
from sklearn import preprocessing
# To split the dataset into train and test datasets
from sklearn.model_selection import train_test_split
# To model the Gaussian Navie Bayes classifier
from sklearn.naive_bayes import GaussianNB
# To calculate the accuracy score of the model
from sklearn.metrics import accuracy_score

from sklearn import preprocessing
le = preprocessing.LabelEncoder()


df = pd.read_csv('./breast-cancer-wisconsin.data.csv')

print(df)

df['F1'] = le.fit_transform(df['F1'])
df['F2'] = le.fit_transform(df['F2'])
df['F3'] = le.fit_transform(df['F3'])
df['F4'] = le.fit_transform(df['F4'])
df['F5'] = le.fit_transform(df['F5'])
df['F6'] = le.fit_transform(df['F6'])
df['F7'] = le.fit_transform(df['F7'])
df['F8'] = le.fit_transform(df['F8'])
df['F9'] = le.fit_transform(df['F9'])

# df.fillna(0)
# print(df.isnull())


# train=df.sample(frac=0.8,random_state=200)
# test=df.drop(train.index)
# print(train, test)

# print(sum(train[value] == '?'))

# print(df)
# print()
# print(df.values[:,:1])

features = df.values[:,1:10]

print(features)

target = df.values[:,10]
features_train, features_test, target_train, target_test = train_test_split(features,
target, test_size = 0.3, random_state = 10)


# print(features_train, features_test, target_train, target_test)
# print(features_train)

# print(len(features_train))
# print(len(features_test))
# print(len(target_train))
# print(len(target_test))

# print(features_train, target_train)

clf = GaussianNB()
clf.fit(features_train, target_train)
target_pred = clf.predict(features_test)

accuracy_rate = accuracy_score(target_test, target_pred, normalize = True)

print(accuracy_rate)

# print(target_train)

# clf = GaussianNB()
# clf.fit(features_train, target_train)
# target_pred = clf.predict(features_test)


# from sklearn.naive_bayes import GaussianNB
# import numpy as np

# #assigning predictor and target variables
# x= np.array([[-3,7],[1,5], [1,2], [-2,0], [2,3], [-4,0], [-1,1], [1,1], [-2,2], [2,7], [-4,1], [-2,7]])
# y = np.array([3, 3, 3, 3, 4, 3, 3, 4, 3, 4, 4, 4])
# #Create a Gaussian Classifier
# model = GaussianNB()

# # Train the model using the training sets 
# model.fit(x, y)

# #Predict Output 
# predicted= model.predict([[1,2],[3,4]])
# print(predicted)

