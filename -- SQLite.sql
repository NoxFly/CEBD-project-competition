WITH sportifsCat AS (
    SELECT numSp
    FROM LesSportifs_base
    WHERE categorieSp = 'masculin'
), A AS (
    SELECT numSp, numEq, pays, categorieSp
    FROM LesEquipiers
    INNER JOIN LesSportifs_base
    USING(numSp)
    WHERE
        numSp IN sportifsCat AND
        pays = 'Belgique'
)
WITH Equipecat AS(
    SELECT numEq, nbEquipiersEq, pays, categorieSp
    FROM LesEquipes
    INNER JOIN A
    USING(numEq)
    GROUP BY numEq
    HAVING COUNT(*) = nbEquipiersEq;
)