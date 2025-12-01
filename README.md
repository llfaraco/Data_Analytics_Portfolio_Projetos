📉 Projeto de Portfólio 3: Modelo de Previsão de Risco de Evasão (Churn)

💡 Objetivo do Projeto

Este projeto move a análise de dados do nível descritivo (o que aconteceu) para o nível preditivo (o que irá acontecer). O objetivo é construir um modelo simples de Machine Learning para identificar, com antecedência, clientes com alto risco de Evasão (Churn) em uma plataforma digital (simulando um e-commerce ou serviço de assinatura).

O valor central deste projeto para o negócio é a Mitigação Proativa de Perdas, permitindo que as equipes de CX, Atendimento e Marketing atuem antes que o cliente desista do serviço, impactando diretamente nas métricas de Retenção e LTV (Lifetime Value).

🛠️ Tecnologias Utilizadas

Linguagem: Python

Análise de Dados: Pandas

Modelagem Estatística: Scikit-learn (Regressão Logística para classificação de risco)

Simulação de Extração: SQL (Representando a etapa de Feature Engineering)

📊 Estrutura e Etapas

O projeto simula um ciclo completo de Data Science, desde a coleta até a recomendação de negócio:

Feature Engineering (Simulação SQL): Definir e extrair as variáveis comportamentais do cliente (frequência de uso, reclamações, inatividade) que indicam risco. (Arquivo: churn_feature_engineering.sql)

Modelagem Preditiva (Python): Treinar o modelo de Regressão Logística para calcular o "Churn Risk Score". (Arquivo: churn_prediction_model.py)

Insight e Recomendação: Traduzir a saída do modelo em uma estratégia de ação de negócio para as equipes de CX e Produto. (Arquivo: Recomendacao_Estrategica_CX.md)

🔑 Insight Central

O modelo demonstrou que a inatividade (último login há mais de 30 dias) combinada com um alto volume de interações negativas com o Suporte (tickets abertos) são os preditores mais fortes de Churn. A ação de negócio deve focar na redução de tickets para clientes novos.

⚙️ Como Executar

Verifique a simulação das features no arquivo SQL.

Execute o script Python: python churn_prediction_model.py

Analise o resultado da classificação e as recomendações estratégicas no arquivo Markdown.

Este projeto demonstra a capacidade de mover a análise do nível descritivo ao preditivo, focando em métricas críticas de negócio como Retenção e LTV.
