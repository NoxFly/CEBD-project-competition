WITH
PaysEquipe AS (
    SELECT numEq, pays
    FROM LesEquipiers
    JOIN LesSportifs_base USING (numSp)
    GROUP BY numEq
)

select numEq from LesEquipes
where numEq IN (
    select numEq from PaysEquipe
    where pays = France
) AND numEq NOT IN (
    select numIn from LesInscriptions
    where numEp = 24
)