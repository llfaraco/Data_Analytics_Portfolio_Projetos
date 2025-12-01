-- =================================================================================
-- SIMULAÇÃO SQL: FEATURE ENGINEERING PARA MODELO DE CHURN
--
-- Esta query representa a etapa de extração, agregação e transformação
-- de dados brutos (transacional, log, atendimento) em features prontas
-- para o Machine Learning.
--
-- Objetivo: Criar variáveis que preveem o risco de CHURN (evasão).
-- Base de Dados: BigQuery (Simulação)
-- =================================================================================

WITH Dados_Comportamentais AS (
    -- 1. Agregação de dados transacionais e de uso
    SELECT
        t1.id_cliente,
        MAX(CURRENT_DATE() - t1.data_ultimo_login) AS dias_inatividade, -- Feature de Longevidade/Engajamento
        AVG(t1.valor_transacao) AS valor_medio_transacao, -- Feature de Valor
        COUNT(DISTINCT t2.id_sessao) AS frequencia_uso_mensal -- Feature de Frequência
    FROM
        tabela_logs_uso t1
    LEFT JOIN
        tabela_sessoes_app t2 ON t1.id_cliente = t2.id_cliente
    WHERE
        t1.data_ultimo_login >= CURRENT_DATE() - INTERVAL '90' DAY -- Filtra clientes ativos no último trimestre
    GROUP BY
        1
),
Dados_Atendimento AS (
    -- 2. Agregação de dados de Experiência e Suporte (CX)
    SELECT
        id_cliente,
        COUNT(id_ticket) AS volume_tickets_ultimos_60d, -- Feature de Atrito
        AVG(csat_score) AS media_csat_ultimos_60d -- Feature de Satisfação
    FROM
        tabela_suporte_tickets
    WHERE
        data_abertura >= CURRENT_DATE() - INTERVAL '60' DAY
    GROUP BY
        1
)
-- 3. Junção (JOIN) e Definição da Variável Alvo (CHURN)
SELECT
    c.id_cliente,
    c.dias_inatividade,
    c.valor_medio_transacao,
    c.frequencia_uso_mensal,
    a.volume_tickets_ultimos_60d,
    a.media_csat_ultimos_60d,
    -- Variável Alvo: Churn. Definida como 1 se o cliente estava ativo 90 dias atrás
    -- mas não fez login nem transacionou nos últimos 30 dias.
    CASE
        WHEN c.dias_inatividade > 30 AND c.valor_medio_transacao IS NULL THEN 1
        ELSE 0
    END AS churn_target -- 1 = Churn, 0 = Ativo
FROM
    Dados_Comportamentais c
LEFT JOIN
    Dados_Atendimento a ON c.id_cliente = a.id_cliente;

-- Nota: Na prática, esta query é o input do dataframe no arquivo Python.