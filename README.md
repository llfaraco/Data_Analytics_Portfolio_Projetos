# Churn | Experimento de classificação com baseline

**Python · scikit-learn · Dados sintéticos · Avaliação em holdout**

Como organizar sinais de uso e atendimento em um experimento de classificação? Este projeto gera 500 clientes sintéticos, separa 400 para treino e 100 para teste e compara regressão logística com um baseline de classe majoritária.

## Executar

Ambiente validado: Python 3.12.

```bash
python -m pip install -r requirements.txt
python churn_prediction_model.py
python -m unittest discover -s tests
```

## Resultado medido na simulação

Semente 42, teste estratificado de 100 registros, limiar de 0,50:

| Métrica | Regressão logística | Baseline |
| --- | ---: | ---: |
| Acurácia | 0,81 | 0,69 |
| Precisão | 0,7143 | 0 |
| Recall | 0,6452 | 0 |
| F1 | 0,6780 | 0 |
| ROC AUC | 0,8121 | 0,50 |

[Resultados e matriz de confusão](artifacts/metrics.json) · [Scores somente do teste](artifacts/holdout_scores.csv) · [Coeficientes](artifacts/coefficients.csv)

**Esses números não representam clientes reais.** O alvo foi construído com inatividade e tickets, então o resultado reflete a regra da simulação. Não há validação externa, temporal, de calibração ou efeito medido em retenção.

## Decisões técnicas

- A separação é estratificada, com semente fixa.
- Imputação e escala ficam em um `Pipeline` ajustado somente no treino.
- O baseline é ajustado com a mesma partição de treino e avaliado no mesmo teste.
- O CSV de scores contém somente IDs de teste, em vez de reaplicar o modelo à base inteira e chamar o resultado de generalização.
- Os coeficientes correspondem a variáveis padronizadas; não são efeitos causais.
- Três testes conferem separação, domínio dos scores, consistência da matriz, baseline e reprodução da base por semente.

A consulta `churn_feature_engineering.sql` permanece um exemplo conceitual, sem tabelas de origem disponíveis. Sua sintaxe e o alvo precisam de adaptação ao banco e ao horizonte temporal real; não é executada pelo Python.

[Como discutir uma aplicação em CX](Recomendacao_Estrategica_CX.md)

Implementação evoluída com assistência de IA, com código, métricas e comandos disponíveis para revisão.

[Portfólio](https://github.com/llfaraco) · [LinkedIn](https://www.linkedin.com/in/lucasrfaraco)
