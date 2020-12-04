-- SQLite
WITH PaysEquipe AS (
    SELECT numEq, pays
    FROM LesEquipiers
    JOIN LesSportifs_base USING (numSp)
    GROUP BY numEq)
-- ), PaysMedailles AS (
--     SELECT pays,
--         SUM(numEq = gold) AS gold,
--         SUM(numEq = silver) AS silver,
--         SUM(numEq = bronze) AS bronze
--     FROM LesResultats
--     JOIN PaysEquipe ON numEq IN (gold, silver, bronze)
--     GROUP BY pays
-- )
SELECT *
FROM PaysEquipe;