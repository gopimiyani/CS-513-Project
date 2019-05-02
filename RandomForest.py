#Importing Libraries

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

#Load Dataset
data = pd.read_csv('DATASET/Final_Refined_Encoded_Normalized.csv')

#Split dataset into its attributes X and labels y
X, y = data.iloc[:, :-1], data.iloc[:, -1]

#Splits the dataset into  train data and  test data by test size
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=2000)

#Scaling the Dataset
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model Training and Calculates the Test & Train accuracy and prints it.
def train_model(X_train, y_train, X_test, y_test, classifier, **kwargs):
    model = classifier(**kwargs)
    model.fit(X_train,y_train)
    
    # check accuracy and print out the results
    fit_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)
    
    print(f"Train accuracy: {fit_accuracy:0.2%}")
    print(f"Test accuracy: {test_accuracy:0.2%}")
    
    return model

if __name__ == "__main__": 
    print("Applying Random Forest...\n")
    # Calls the above function to train the Data for Random Forest

    model = train_model(X_train, y_train, X_test, y_test, RandomForestClassifier, random_state=1000)
    pd.Series(model.feature_importances_,X.columns).sort_values(ascending=False)[0:25].plot.barh()