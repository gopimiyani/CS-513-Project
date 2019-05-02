import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn import svm, datasets
from sklearn.model_selection import GridSearchCV

df = pd.read_csv('./Final_Refined_Encoded_Normalysed.csv')
# parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}

# features = df[['screen_to_body_ratio']].values[:,:]
df0 = df[['SIM', 'CPU', 'GPU', 'memory_card', 'weight_g', 'screen_to_body_ratio', \
    'primary_camera', 'internal_memory', 'Thickness',\
    'display_size', 'OS', 'radio', 'RAM', 'EDGE'\
    ]]
#df0 = df[['primary_camera', 'weight_g']]
features = df0.values[:,:]

df1 = df[['Price']]
target = df1.values[:,0]
# print(features)
# print(target)

# parameters = {'kernel':('linear', 'rbf'), 'C':[1, 10]}
# svc = svm.SVC(gamma="scale")
# clf = GridSearchCV(svc, parameters, cv=5)
# clf.fit(features, target)
# print(sorted(clf.cv_results_.keys()))

features_train, features_test, target_train, target_test = train_test_split(features,
target, test_size = 0.3, random_state = 10)

clf = GaussianNB()
clf.fit(features_train, target_train)
target_pred = clf.predict(features_test)
accuracy_rate = accuracy_score(target_test, target_pred, normalize = True)

print(accuracy_rate)
fo = open("./nb_result.txt", "w")
fo.write(str(accuracy_rate))
fo.close()
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

