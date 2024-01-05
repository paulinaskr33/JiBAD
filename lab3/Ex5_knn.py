import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  # pomoze w standaryzacji danych
from sklearn.neighbors import KNeighborsClassifier  # wczytujemy klasyfikator
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix  # pomoze zwizualizowac krzywe oceniajace poprawnosc
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('rozpoznawanie_falszywych_pieniedzy.csv', sep=';')
print(dataset.head())  # wyswietlam 5 pierwszych wierszy

dataset.dropna(inplace=True)  # odrzucam puste komorki

X = dataset[['diagonal', 'height_left', 'height_right', 'margin_low', 'margin_up', 'length']]
y = dataset['is_genuine']

# rozdzielam zbiory treningowe i testowe

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# random_state to hiperparametr odpowiedzialny za losowosc, 42 jest common wartoscia

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # fit_transform() wyciagnie srednia i wariancje
X_test = scaler.transform(X_test)

k_values = [1, 2, 3, 5, 7]

auc_values = []

for k in k_values:
    # Tworze klasyfikator knn dla kazdego konkretnego k
    knn_classifier = KNeighborsClassifier(n_neighbors=k)

    # Trenuje klasyfikator knn
    knn_classifier.fit(X_train, y_train)

    # Pozytywne prawdopodobienstwa
    y_scores = knn_classifier.predict_proba(X_test)[:, 1]

    # Obliczam AUC
    auc = roc_auc_score(y_test, y_scores)

    # Obliczam macierz bledu
    y_pred = knn_classifier.predict(X_test)
    conf_matrix = confusion_matrix(y_test, y_pred)

    # Określenie optymalnego Progu Granicznego/Odcięcia
    fp, tp, _ = roc_curve(y_test, y_scores)
    optimal_threshold = tp[np.argmax(tp - fp)]

    # Dodaje AUC
    auc_values.append(auc)

    # Rysuje ROC dla konkretnego k
    plt.figure()
    plt.plot(fp, tp)
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'ROC Curve for KNN with k = {k} (AUC = {auc:.2f})')
    plt.show()

    # Rysuje AUC, Confusion Matrix, and Cutoff Threshold dla k
    print("AUC for KNN with k =", k, ":", auc)
    print("Confusion Matrix for KNN with k =", k, ":\n", conf_matrix)
    print("Optimal Cutoff Threshold for KNN with k =", k, ":", optimal_threshold)

# Rysuje AUC dla roznych k
plt.figure()
plt.plot(k_values, auc_values, marker='o')
plt.xlabel('k Value')
plt.ylabel('AUC')
plt.title('AUC for Different K Values (Binary Classification)')
plt.grid()
plt.show()