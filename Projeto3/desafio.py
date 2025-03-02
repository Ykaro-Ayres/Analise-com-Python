# -*- coding: utf-8 -*-
"""Desafio.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13hjbkHnXwtcHrZb4EB-jzofnCurVg6-R
"""

#Etapa 1
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score

# a) Carregar a base de dados
streaming_data = pd.read_csv("streaming_data.csv")

# b) Descrição estatística dos dados
print("Descrição estatística dos dados:")
print(streaming_data.describe())

# c) Verificar os tipos de dados
print("\nTipos de dados:")
print(streaming_data.dtypes)

# d) Quantidade de valores faltantes
print("\nQuantidade de valores faltantes:")
print(streaming_data.isna().sum())

# Etapa 02
# Substituir valores NaN por 0
cols_to_fillna = ["Time_on_platform", "Num_streaming_services", "Avg_rating", "Devices_connected"]
streaming_data[cols_to_fillna] = streaming_data[cols_to_fillna].fillna(0)

# Dropar linhas nulas nas colunas Gender, Subscription_type e Age
streaming_data.dropna(subset=["Gender", "Subscription_type", "Age"], inplace=True)

# Transformar valores churned 0 e 1 por No e Yes
streaming_data["Churned"] = streaming_data["Churned"].replace({0: "No", 1: "Yes"})

# Remover linhas com valores nulos
streaming_data.dropna(inplace=True)

# Etapa 03
# Definir X e y
X = streaming_data.drop(columns=["Churned"])  # Features
y = streaming_data["Churned"]  # Target variable

from sklearn.preprocessing import OneHotEncoder

# Codificar variáveis
encoder = OneHotEncoder(drop='first', sparse=False)
X_encoded = pd.DataFrame(encoder.fit_transform(X.select_dtypes(include=['object'])))

# Dividir os dados codificados em conjunto de treinamento e teste
X_train_encoded, X_test_encoded, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Treinar o modelo de regressão logística com os dados codificados
log_reg_model = LogisticRegression()
log_reg_model.fit(X_train_encoded, y_train)

from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Definir variáveis categóricas e numéricas
categorical_features = ["Gender", "Subscription_type"]
numerical_features = ["Time_on_platform", "Num_streaming_services", "Avg_rating", "Devices_connected"]

# Codificar variáveis categóricas
encoder = OneHotEncoder(drop='first', sparse=False)
encoder.fit(streaming_data[categorical_features])
X_encoded = encoder.transform(streaming_data[categorical_features])

# Dividir os dados em conjunto de treinamento e teste
X_train_encoded, X_test_encoded, y_train, y_test = train_test_split(X_encoded, streaming_data["Churned"], test_size=0.2, random_state=42)

# Obter índices correspondentes para os dados numéricos
train_indices = np.arange(len(X_train_encoded))
test_indices = np.arange(len(X_test_encoded))

# Obter dados numéricos correspondentes aos índices
X_train_numerical = streaming_data.iloc[train_indices][numerical_features].values
X_test_numerical = streaming_data.iloc[test_indices][numerical_features].values

# Concatenar variáveis codificadas com variáveis numéricas
X_train_final = np.concatenate([X_train_encoded, X_train_numerical], axis=1)
X_test_final = np.concatenate([X_test_encoded, X_test_numerical], axis=1)

# Treinar o modelo de regressão logística
log_reg_model = LogisticRegression()
log_reg_model.fit(X_train_final, y_train)

# Fazer previsões usando o modelo treinado
y_pred = log_reg_model.predict(X_test_final)

# Avaliar o modelo
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

from sklearn.preprocessing import LabelEncoder, MinMaxScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Definir variáveis X e y para o modelo
X = streaming_data.drop(columns=["Churned"])
y = streaming_data["Churned"]

# Codificar variáveis categóricas
encoder = OneHotEncoder(drop='first', sparse=False)
X_encoded = pd.DataFrame(encoder.fit_transform(X.select_dtypes(include=['object'])))

# Separar em conjunto de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Realizar o .fit do modelo
log_reg_model = LogisticRegression()
log_reg_model.fit(X_train, y_train)

# Realizar a modelagem
y_pred = log_reg_model.predict(X_test)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Plotar matrix confusão
conf_matrix = confusion_matrix(y_test, y_pred, labels=log_reg_model.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=log_reg_model.classes_)
disp.plot(cmap=plt.cm.Blues)
plt.title("Matriz de Confusão")
plt.show()

# Printar métricas
accuracy = log_reg_model.score(X_test, y_test)
print("Accuracy:", accuracy)

#Etapa 5
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.feature_selection import SelectKBest, chi2

# Carregar os dados
streaming_data = pd.read_csv("streaming_data.csv")

# Tratamento dos dados
streaming_data.dropna(subset=["Gender", "Subscription_type", "Age"], inplace=True)
streaming_data["Churned"] = streaming_data["Churned"].replace({0: "No", 1: "Yes"})
streaming_data.dropna(inplace=True)

# Definir features e target
X = streaming_data.drop(columns=["Churned"])
y = streaming_data["Churned"]

# Codificar variáveis categóricas
X_encoded = pd.get_dummies(X, drop_first=True)

# Dividir os dados em conjunto de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)

# Selecionar as melhores features usando chi-quadrado
selector = SelectKBest(score_func=chi2, k=10)
X_train_selected = selector.fit_transform(X_train, y_train)

# Inicializar o modelo Random Forest
rf_model = RandomForestClassifier()

# Ajustar o modelo aos dados de treinamento
rf_model.fit(X_train_selected, y_train)

# Realizar previsões nos dados de teste
X_test_selected = selector.transform(X_test)
y_pred = rf_model.predict(X_test_selected)

# Avaliar o modelo
conf_matrix = confusion_matrix(y_test, y_pred)
accuracy = accuracy_score(y_test, y_pred)
classification_rep = classification_report(y_test, y_pred)

# Imprimir resultados
print("Matriz de Confusão:")
print(conf_matrix)
print("\nAcurácia:", accuracy)
print("\nRelatório de Classificação:")
print(classification_rep)