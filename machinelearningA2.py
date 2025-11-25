import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

points1 = np.array([[2, 3], [5, 8], [1, 1], [8, 8], [7, 3]])

centroids = np.array([[2, 3], [8, 8]])

while True:
    distances = np.linalg.norm(points1[:, None] - centroids[None, :], axis=2)
    labels = np.argmin(distances, axis=1)

    new_centroids = np.array([points1[labels == i].mean(axis=0) for i in range(2)])

    if np.allclose(new_centroids, centroids):
        break

    centroids = new_centroids

print("Final centroids:", centroids)
print("Cluster assignments:", labels)

print ('assignment 1 finished')

points2 = np.array([[1, 2], [2, 3], [6, 6], [8, 8], [10, 10]])

linked = sch.linkage(points2, method='single', metric='euclidean')

print("Linkage matrix:\n", linked)

plt.figure(figsize=(6, 4))
sch.dendrogram(linked, labels=[str(p) for p in points2])
plt.title("Hierarchical Clustering Dendrogram")
plt.xlabel("Data Points")
plt.ylabel("Euclidean Distance")
plt.show()

print ('assignment 2 finished')

points3 = np.array([
    [1, 2],
    [2, 3],
    [3, 3.5],
    [5, 6],
    [7, 8],
    [25, 80]
])

model = IsolationForest(contamination=0.2, random_state=999)
model.fit(points3)

# Predict anomalies (-1 = anomaly, 1 = normal)
labels = model.predict(points3)

print("Points:")
print(points3)
print("Anomaly detection (1 = normal, -1 = anomaly):")
print(labels)

print ('assignment 3 finished')

X = np.array([
    [2, 4],
    [3, 6],
    [4, 8],
    [5, 10],
    [6, 12]
])

X_mean = X.mean(axis=0)
X_std = X.std(axis=0, ddof=1)
X_standardized = (X - X_mean) / X_std

print("Standardized Data:\n", X_standardized)

#Covariance Matrix
cov_matrix = np.cov(X_standardized.T)
print("\nCovariance Matrix:\n", cov_matrix)

eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

print("\nEigenvalues:", eigenvalues)
print("Eigenvectors (columns):\n", eigenvectors)

# Sort eigenvalues/eigenvectors by largest
idx = np.argsort(eigenvalues)[::-1]
eigenvalues = eigenvalues[idx]
eigenvectors = eigenvectors[:, idx]

print("\nSorted Eigenvalues:", eigenvalues)
print("Sorted Eigenvectors:\n", eigenvectors)


pc1 = eigenvectors[:, 0]
X_pca = X_standardized.dot(pc1)

print("\nProjection onto 1st Principal Component:\n", X_pca)

print('assignment 4 finished') 



