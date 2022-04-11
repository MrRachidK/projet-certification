import sys
sys.path.insert(0, '../')
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import joblib

df = pd.read_csv("data/data.csv")

X = df[["Height", "Weight"]]
y = df["Species"]

clf = GaussianNB() 
clf.fit(X, y)

joblib.dump(clf, "src/clf.pkl")
