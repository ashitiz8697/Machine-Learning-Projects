import pandas as pd
import numpy as np
import os
from sklearn.tree import DecisionTreeClassifier

DOWNLOAD_ROOT = "https://s3-api.us-geo.objectstorage.softlayer.net/cf-courses-data/CognitiveClass/ML0101ENv3/labs/FuelConsumptionCo2.csv"
DATASET_PATH = os.path.join("../","datasets")
csv_file_path = os.path.join(DATASET_PATH,"drug200.csv")

my_data = pd.read_csv(csv_file_path)
print(my_data.head()) 
print(my_data.size)
X = my_data[['Age','Sex','BP','Cholesterol','Na_to_K']].values
print(X[0:5])

##
## PRE-PROCESSING
##

from sklearn import preprocessing
le_sex = preprocessing.LabelEncoder()
le_sex.fit(['F','M'])
X[:,1] = le_sex.transform(X[:,1])

le_BP = preprocessing.LabelEncoder()
le_BP.fit(['LOW','NORMAL','HIGH'])
X[:,2] = le_BP.transform(X[:,2])

le_chol = preprocessing.LabelEncoder()
le_chol.fit(['NORMAL','HIGH'])
X[:,3] = le_chol.transform(X[:,3])
print('########### AFTER TRANSFORM #############')
print(X[0:5])

y= my_data['Drug']
print("######### DRUG DATA ###########")
print(y[0:5])

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3,random_state=3)
print(X_train.shape)

drugTree = DecisionTreeClassifier(criterion="entropy",max_depth = 4)
print(drugTree)
drugTree.fit(X_train,y_train)

predTree = drugTree.predict(X_test)

print(predTree[0:5])
print(y_test[0:5])

from sklearn import metrics
import matplotlib.pyplot as plt

print("DecisonTree's Accuracy :: ", metrics.accuracy_score(y_test,predTree))

from sklearn.externals.six import StringIO
import pydotplus
import matplotlib.image as mpimg
from sklearn import tree

dot_data = StringIO()
filename = "drugtree.png"
featureNames = my_data.columns[0:5]
targetNames = my_data["Drug"].unique().tolist()
out =tree.export_graphviz(drugTree,feature_names = featureNames,out_file=dot_data,class_names=np.unique(y_train),filled=True,special_characters=True,rotate=False)
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
graph.write_png(filename)
img = mpimg.imread(filename)
plt.figure(figsize=(100,200))
#plt.imshow(img.interpolation='nearest')
