import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
import numpy as np

# ==============================================================================
# 1. Simulação dos Dados (Feature Engineering e Extração SQL)
#
# Na vida real, estes dados seriam o resultado final da query em
# churn_feature_engineering.sql, após a limpeza e transformação.
#
# Features:
# - dias_inatividade: Dias desde o último login/uso. (Alto = Risco)
# - volume_tickets_ultimos_60d: Nº de tickets abertos recentemente. (Alto = Risco)
# - valor_medio_transacao: Média de gasto do cliente. (Baixo = Risco)
# - churn: Variável alvo (1 = Saiu, 0 = Não saiu).
# ==============================================================================

# Gerando dados simulados para 500 clientes
np.random.seed(42)
data_size = 500
df = pd.DataFrame({
    'id_cliente': range(1, data_size + 1),
    'dias_inatividade': np.random.randint(0, 100, data_size),
    'volume_tickets_ultimos_60d': np.random.randint(0, 5, data_size),
    'valor_medio_transacao': np.random.uniform(50, 500, data_size),
    'frequencia_uso_mensal': np.random.randint(1, 30, data_size),
})

# Criando a variável alvo 'churn' de forma correlacionada:
# Clientes inativos E com muitos tickets são mais propensos a dar churn
df['churn'] = ((df['dias_inatividade'] > 60) & (df['volume_tickets_ultimos_60d'] >= 2)).astype(int)
df.loc[df.sample(frac=0.1, random_state=1).index, 'churn'] = 1 # Adiciona ruído de churn

# Definindo as features (variáveis preditoras)
FEATURES = [
    'dias_inatividade',
    'volume_tickets_ultimos_60d',
    'valor_medio_transacao',
    'frequencia_uso_mensal'
]

X = df[FEATURES]
y = df['churn']

# ==============================================================================
# 2. Preparação e Treinamento do Modelo Preditivo
# ==============================================================================

# Dividindo dados em treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalizando as features (essencial para Regressão Logística)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Treinando o modelo (Regressão Logística, simples e interpretável)
model = LogisticRegression(solver='liblinear', random_state=42)
model.fit(X_train_scaled, y_train)

# ==============================================================================
# 3. Avaliação e Geração do Churn Risk Score
# ==============================================================================

# Previsão no conjunto de testes
y_pred = model.predict(X_test_scaled)
# y_proba = model.predict_proba(X_test_scaled)[:, 1] # Probabilidade de Churn

print("=====================================================================")
print("### 📉 Avaliação do Modelo de Previsão de CHURN")
print("=====================================================================")

# Acurácia
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do Modelo no Teste: {accuracy * 100:.2f}%\n")

# Coeficientes: Mostra a importância de cada feature (interpretabilidade)
print("### Coeficientes do Modelo (Importância das Features):")
feature_importance = pd.Series(model.coef_[0], index=FEATURES).sort_values(ascending=False)
print(feature_importance.to_markdown(numalign="left", stralign="left"))
print("\n*Um coeficiente positivo indica que a feature aumenta o risco de Churn.")


# ==============================================================================
# 4. Geração do Churn Risk Score (O Insight para a Ação de Negócio)
# ==============================================================================

# Aplicando o modelo em toda a base de dados (simulação de clientes "ativos")
df['churn_risk_score'] = model.predict_proba(scaler.transform(X))[:, 1]

# Identificando clientes de ALTO RISCO (probabilidade > 50%)
df_alto_risco = df[df['churn_risk_score'] > 0.50].sort_values(by='churn_risk_score', ascending=False)

print("\n=====================================================================")
print(f"### 🎯 Lista de Clientes de ALTO RISCO ({len(df_alto_risco)} encontrados)")
print("=====================================================================")

# Resultado: Lista de clientes que a equipe de CX deve abordar PROATIVAMENTE
print(df_alto_risco[['id_cliente', 'churn_risk_score', 'dias_inatividade', 'volume_tickets_ultimos_60d']].head(10).to_markdown(index=False, numalign="left", stralign="left"))

print("\n---")
print("A saída do modelo é uma lista acionável. A recomendação estratégica para o negócio está no arquivo Recomendacao_Estrategica_CX.md.")