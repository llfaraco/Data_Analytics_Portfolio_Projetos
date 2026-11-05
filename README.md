# Churn | Modelo didático de risco e recomendação para CX

**Projeto de estudo · Python · scikit-learn · SQL conceitual**

## Problema

Como transformar sinais de uso e atendimento em uma lista de clientes que merecem investigação por uma equipe de retenção?

O projeto simula esse fluxo com dados sintéticos. Não utiliza uma carteira real e não demonstra redução de churn em produção.

## O que o código faz

1. Gera **500 clientes sintéticos** com semente aleatória definida.
2. Cria um alvo de churn a partir de regras de inatividade e tickets, com ruído adicional.
3. Separa treino e teste.
4. Ajusta `StandardScaler` no treino e treina regressão logística.
5. Imprime acurácia e coeficientes.
6. Calcula scores e apresenta exemplos acima do limiar de 0,50.

## Arquivos

| Arquivo | Papel |
| --- | --- |
| `churn_prediction_model.py` | Geração de dados, treinamento, avaliação e scores |
| `churn_feature_engineering.sql` | Exemplo conceitual de extração e agregação de variáveis |
| `Recomendacao_Estrategica_CX.md` | Proposta de leitura e ação para CX; não é evidência de efeito medido |

A consulta SQL descreve tabelas hipotéticas e não é executada pelo Python. Sua sintaxe e as regras de negócio precisam de adaptação ao banco e ao cenário real.

## Como executar

Na raiz, em um ambiente Python:

```bash
python -m pip install pandas numpy scikit-learn tabulate
python churn_prediction_model.py
```

A execução não foi validada nesta revisão documental.

## Como interpretar

O alvo foi construído com as próprias variáveis de inatividade e tickets. Portanto, o desempenho e os coeficientes refletem em parte **a regra da simulação**, não uma descoberta validada sobre clientes reais.

A lista final aplica o modelo a toda a base simulada, incluindo exemplos utilizados no treino. Ela demonstra o formato de uma saída; não mede generalização.

## Evolução

Avaliar precision, recall, matriz de confusão e custo dos erros; comparar um baseline; estudar calibração e validação temporal; definir ações com a área de negócio e medir seus efeitos em dados reais autorizados.

## Contato

[Lucas Faraco](https://www.linkedin.com/in/lucasrfaraco) · [E-mail](mailto:lucas.rfaraco@gmail.com) · [Perfil e portfólio](https://github.com/llfaraco)
