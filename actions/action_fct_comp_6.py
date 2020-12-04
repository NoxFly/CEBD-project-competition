
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 4
class AppFctComp6(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_6.ui", self)
        self.data = data
        self.refreshCatList()

    # Fonction de mise à jour des catégories
    @pyqtSlot()
    def refreshCatList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("""WITH
                PaysEquipe AS (
                    SELECT numEq, pays
                    FROM LesEquipiers
                    JOIN LesSportifs_base USING (numSp)
                    GROUP BY numEq
                ),
                PaysMedailles AS (
                    SELECT pays,
                        SUM(numEq = gold) AS gold,
                        SUM(numEq = silver) AS silver,
                        SUM(numEq = bronze) AS bronze
                    FROM LesResultats
                    JOIN PaysEquipe ON numEq IN (gold, silver, bronze)
                    GROUP BY pays
                    UNION ALL
                    SELECT pays, 
                        SUM(numSp = gold) AS gold,
                        SUM(numSp = silver) AS silver,
                        SUM(numSp = bronze) AS bronze
                    FROM LesResultats
                    JOIN LesSportifs_base ON numSp IN (gold, silver, bronze)
                    GROUP BY pays
                )
                SELECT pays, SUM(gold) AS nbOr, SUM(silver) AS nbArgent, SUM(bronze) AS nbBronze 
                FROM PaysMedailles
                GROUP BY pays
                ORDER BY nbOr DESC, nbArgent DESC, nbBronze DESC""")
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_6, "Une erreur est survenue : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_6, result)

            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_6, "Aucun résultat")