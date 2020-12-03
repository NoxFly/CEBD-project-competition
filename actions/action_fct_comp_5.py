
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 4
class AppFctComp5(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_5.ui", self)
        self.data = data
        self.refreshCatList()

    # Fonction de mise à jour des catégories
    @pyqtSlot()
    def refreshCatList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("""SELECT E.numEq, M.pays, E.nbEquipiersEq, MIN(M.ageSp) AS minAge, MAX(M.ageSp) AS maxAge, ROUND(AVG(M.ageSp)) AS moyenneAge
                FROM LesEquipes E
                JOIN (
                    SELECT S.numSP, E.numEq, S.ageSp, S.pays
                    FROM LesSportifs S
                    LEFT JOIN LesEquipiers E
                    ON S.numSp = E.numSp
                    WHERE E.numEq IS NOT NULL
                ) AS M
                ON E.numEq = M.numEq
                JOIN LesResultats R
                ON E.numEq = R.gold
                GROUP BY E.numEq
                ORDER BY E.numEq""")
        except Exception as e:
            display.refreshLabel(self.ui.label_fct_comp_5, "Une erreur est survenue")
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_5, result)

            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_5, "Aucun résultat")