# Da análise à decisão de retenção

Este experimento usa dados sintéticos. Nenhuma ação abaixo foi aplicada a clientes reais, nem há redução de churn medida.

## Leitura do experimento

O alvo foi criado por uma regra de inatividade e volume de tickets. O modelo aprende parte dessa regra. As métricas em `artifacts/metrics.json` servem para estudar treino, teste, comparação com baseline e classificação.

A matriz de confusão usa linhas = real, colunas = previsto, na ordem [0, 1]. A precisão mede quantos positivos previstos eram positivos; o recall mede quantos positivos reais foram recuperados. O limiar de 0,50 é didático.

## Hipótese de aplicação

Em um cenário real autorizado, investigar fricções de atendimento e queda de uso antes de propor uma intervenção. Definir com CX o que é cancelamento, qual a data de previsão e qual janela futura será observada.

## Antes de uso operacional

- Separar clientes e períodos de treino e avaliação; usar somente variáveis disponíveis na data da decisão.
- Comparar com regras simples e avaliar o custo dos falsos positivos e negativos.
- Verificar representatividade, privacidade, qualidade e estabilidade dos dados.
- Validar calibração e escolher o limiar de acordo com a capacidade de atendimento.
- Medir a intervenção com um desenho adequado, como experimento com grupo de comparação.

Um score sozinho não demonstra que a ação melhora retenção. Esse efeito precisaria ser medido.
