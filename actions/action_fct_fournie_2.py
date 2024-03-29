
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic

# Classe permettant d'afficher la fonction fournie 2
class AppFctFournie2(QDialog):

    #Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_fournie_2.ui", self)
        self.data = data

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        display.refreshLabel(self.ui.label_fct_fournie_2, "")

        if not self.ui.lineEdit.text().strip():
            self.ui.table_fct_fournie_2.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_fournie_2, "Veuillez indiquer un numéro d'équipe")

        else:
            try:
                result = self.data.cursor().execute("SELECT nomSp, prenomSp, pays, categorieSp FROM LesSportifs_base INNER JOIN LesEquipiers USING (numSp) WHERE numEq=?", [self.ui.lineEdit.text().strip()])
            
            except Exception as e:
                self.ui.table_fct_fournie_2.setRowCount(0)
                display.refreshLabel(self.ui.label_fct_fournie_2, "Impossible d'afficher les résultats : " + repr(e))

            else:
                if display.refreshGenericData(self.ui.table_fct_fournie_2, result) == 0:
                    display.refreshLabel(self.ui.label_fct_fournie_2, "Aucun résultat")