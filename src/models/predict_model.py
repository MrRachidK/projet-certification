# Import of the libraries
import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from config import basedir
from src.features.build_features import train_df

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

import joblib

# Import of the data
print(train_df)
y_train_full = train_df['Winner']
x_train_full = train_df.drop('Winner', axis=1)

# Preparation of the model
x_train, x_cv, y_train, y_cv = train_test_split(x_train_full, y_train_full, test_size=0.2, random_state=42)

clf_dict = {'log reg': LogisticRegression(), 
            'naive bayes': GaussianNB(), 
            'random forest': RandomForestClassifier(n_estimators=100),
            'knn': KNeighborsClassifier(),
            'linear svc': LinearSVC(),
            'ada boost': AdaBoostClassifier(n_estimators=100),
            'gradient boosting': GradientBoostingClassifier(n_estimators=100),
            'CART': DecisionTreeClassifier()}

models_results = {}

# Model training
for name, clf in clf_dict.items():
    model = clf.fit(x_train, y_train)
    pred = model.predict(x_cv)
    print('Accuracy of {}:'.format(name), accuracy_score(pred, y_cv))
    models_results[name] = (model, accuracy_score(pred, y_cv))

# Sort dict by values
models_results = sorted(models_results.items(), key=lambda x: x[1][1], reverse=True)
print(models_results)
best_model = models_results[0][1][0]
print(best_model)

joblib.dump(best_model, os.path.join(basedir, 'src/models/clf.pkl'))
