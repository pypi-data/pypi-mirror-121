import numpy as np
import pandas as pd
from fgroups.groups import PermutationGroup
import time
import random
import requests

n = 8
subset = [np.arange(n)]
perm_group = PermutationGroup(subset=subset)
full_group = perm_group.generate_group().group_

url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.csv"
df = pd.read_csv(url, header=None)

X = df[df.columns[[0, 1, 2, 3, 4, 5, 6, 7]]].values
y = df[df.columns[8]].values
n_rows = X.shape[0]
n_cols = X.shape[1]
classes = np.unique(y)
n_classes = len(classes)
print(f"Numbers of Examples: {n_rows}")
print(f"Number of Inputs: {n_cols}")
print(f"Number of Classes: {n_classes}")
print(f"Classes: {classes}")
print("Class Breakdown:")
breakdown = ""
for c in classes:
	total = len(y[y == c])
	ratio = (total / float(len(y))) * 100
	print(f" - Class {str(c)}: {total} ({ratio:.1f}%)")


