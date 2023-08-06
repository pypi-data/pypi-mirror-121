import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix


# path = 'C:\\Users\\DELL\\Documents\\GitHub\\credit_data.csv'

# df = pd.read_csv(path)
# print(df.head())

def predict_classification_df(df, label, classifier, knn_neighbors=None):
    if knn_neighbors != None:
        n_neighbors = knn_neighbors
    else:
        n_neighbors = 3
    list = []
    
    for i in df.columns:
        if df[i].dtype != 'object':
            list.append(i)
            
    df = df[list]
    #print(df.isnull().sum())
    print(f"The size of the dataframe is {len(df)}")
    df = df.dropna()
    print(f"The size of the dataframe after dropping NaN values is {len(df)}")

    X = df.drop(label, axis="columns")
    #print(X)
    y = df[label]

    X_train, X_test, y_train, y_test = train_test_split(X, y,test_size=0.2, random_state=101)
    sc_x = StandardScaler()
    X_train = sc_x.fit_transform(X_train) 
    X_test = sc_x.transform(X_test)

    if classifier == 'logistic':
        model = LogisticRegression()
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        print(confusion_matrix(y_test, predictions))
        print(classification_report(y_test, predictions))
        return print(model.score(X_test, y_test))
    
    if classifier == 'knn':
        print('yes')
        knn_algo = KNeighborsClassifier(n_neighbors)
 
        knn_algo.fit(X_train, y_train)
        predictions = knn_algo.predict(X_test)
        print(confusion_matrix(y_test, predictions))

        print(classification_report(y_test, predictions))
        return print(f"The test accuracy is {knn_algo.score(X_test, y_test)}")
 

    

    





    



# clean_classification_df(df, 'CARDHLDR', 'knn')