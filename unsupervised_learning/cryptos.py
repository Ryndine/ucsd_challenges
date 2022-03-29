import pandas as pd
from path import Path
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

crypto_df = pd.read_csv(R"crypto_data.csv", index_col=0)

# Select coins that are trading
crypto_trading = crypto_df.loc[crypto_df['IsTrading'] == True]
# print(cyrpto_trading['IsTrading'].value_counts)

crypto_trading = crypto_trading.drop('IsTrading', axis=1)

#Drop null values
crypto_trading = crypto_trading.dropna()

# Filter for cryptocurrencies that have been mined.
crypto_trading = crypto_trading[crypto_trading['TotalCoinsMined'] > 0]

# Delete the `CoinName` from the original dataframe.
crypto_trading = crypto_trading.drop('CoinName', axis=1)
# print(crypto_trading)

# Convert the remaining features with text values, `Algorithm` and `ProofType`, into numerical data.
X = pd.get_dummies(data=crypto_trading, columns=['Algorithm', 'ProofType'])

# print(crypto_trading)
# print(X)

# Standardize your dataset
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#  Dimensionality Reduction
pca = PCA(n_components=.90)
components = pca.fit_transform(X_scaled)

# print(pca.explained_variance_.sum())
# Number explained features dropped significantly.

tsne = TSNE(perplexity=50)
tsne_features = tsne.fit_transform(components)

X = tsne_features[:,0]
y = tsne_features[:,1]

plt.scatter(X, y)
plt.show()

# Cluster Analysis with k-Mean
inertia = []
k = list(range(1,11))

for i in k:
    kmeans = KMeans(n_clusters=i, random_state=0)
    kmeans.fit(components)
    inertia.append(kmeans.inertia_)

elbow = pd.DataFrame({'k': k, 'inertia': inertia})
elbow.plot.line(x='k', y='inertia')

plt.ylabel('inertia')
plt.title('elbow plot')
plt.show()

# Both analysis show no clustering for the provided data.