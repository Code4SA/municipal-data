BEGIN;

\echo Create import table...

CREATE TEMPORARY TABLE conditional_grant_upsert
(
        demarcation_code TEXT,
        period_code TEXT,
        grant_code TEXT,
        amount DECIMAL
) ON COMMIT DROP;

\echo Read data...

\copy conditional_grant_upsert (demarcation_code, period_code, grant_code, amount) FROM '' DELIMITER ',' CSV HEADER;

\echo Delete demarcation_code-period_code pairs that are in the update

DELETE FROM conditional_grant_facts f WHERE EXISTS (
        SELECT 1 FROM conditional_grant_upsert i
        WHERE f.demarcation_code = i.demarcation_code
        AND f.period_code = i.period_code
        LIMIT 1
    );

\echo Insert new values...

INSERT INTO conditional_grant_facts
(
    demarcation_code,
    period_code,
    grant_code,
    amount,
    financial_year,
    amount_type_code,
    period_length,
    financial_period
)
SELECT demarcation_code,
       period_code,
       grant_code,
       amount,
       cast(left(period_code, 4) as int),
       case when period_code ~ '^\d{4}(ADJB|ORGB|SCHD|TRFR)(M\d{2})?$'
               then substr(period_code, 5, 4)
           when period_code ~ '^\d{4}M\d{2}$'
               then 'ACT'
       end,
       case when period_code ~ '^\d{4}M\d{2}$'
                then 'month'
            when period_code ~ '^\d{4}(ADJB|ORGB|SCHD|TRFR)$'
                then 'year'
       end,
       case when period_code ~ '^\d{4}M\d{2}$'
                then cast(right(period_code, 2) as int)
            when period_code ~ '^\d{4}(ADJB|ORGB|SCHD|TRFR)$'
                then cast(left(period_code, 4) as int)
       end
FROM conditional_grant_upsert i;

COMMIT;
