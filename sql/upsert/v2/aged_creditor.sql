\set ON_ERROR_STOP on

BEGIN;

\echo Create import table...

CREATE TEMPORARY TABLE aged_creditor_upsert
(
        demarcation_code TEXT,
        period_code TEXT,
        item_code TEXT,
        g1_amount DECIMAL,
        l1_amount DECIMAL,
        l120_amount DECIMAL,
        l150_amount DECIMAL,
        l180_amount DECIMAL,
        l30_amount DECIMAL,
        l60_amount DECIMAL,
        l90_amount DECIMAL,
        total_amount DECIMAL
) ON COMMIT DROP;

\echo Read data...

\copy aged_creditor_upsert (demarcation_code, period_code, item_code, g1_amount, l1_amount, l120_amount, l150_amount, l180_amount, l30_amount, l60_amount, l90_amount, total_amount) FROM '' DELIMITER ',' CSV HEADER;

\echo Delete demarcation_code-period_code pairs that are in the update

DELETE FROM aged_creditor_facts_v2 f WHERE EXISTS (
        SELECT 1 FROM aged_creditor_upsert i
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
    );

\echo Insert new values...

INSERT INTO aged_creditor_facts_v2
(
    demarcation_code,
    period_code,
    item_id,
    g1_amount,
    l1_amount,
    l120_amount,
    l150_amount,
    l180_amount,
    l30_amount,
    l60_amount,
    l90_amount,
    total_amount,
    financial_year,
    amount_type_id,
    period_length,
    financial_period
)
SELECT demarcation_code,
       period_code,
       (select id from aged_creditor_items_v2 where aged_creditor_items_v2.code = item_code),
       g1_amount,
       l1_amount,
       l120_amount,
       l150_amount,
       l180_amount,
       l30_amount,
       l60_amount,
       l90_amount,
       total_amount,
       cast(left(period_code, 4) as int),
       case when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD|ITY1|ITY2|TABB)(M\d{2})?$'
               then (select id from amount_type_v2 where amount_type_v2.code = substr(period_code, 5, 4))
           when period_code ~ '^\d{4}M\d{2}$'
               then (select id from amount_type_v2 where amount_type_v2.code = 'ACT')
       end,
       case when period_code ~ '^\d{4}M\d{2}$'
                then 'month'
            when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD|ITY1|ITY2|TABB)$'
                then 'year'
       end,
       case when period_code ~ '^\d{4}M\d{2}$'
                then cast(right(period_code, 2) as int)
            when period_code ~ '^\d{4}(IBY1|IBY2|ADJB|ORGB|AUDA|PAUD|ITY1|ITY2|TABB)$'
                then cast(left(period_code, 4) as int)
       end
FROM aged_creditor_upsert i;

COMMIT;