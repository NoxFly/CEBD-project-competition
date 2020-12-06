
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 2

class AppFctComp2(QDialog):
    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_2.ui", self)
        self.data = data
        self.refreshCatList()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        display.refreshLabel(self.ui.label_fct_comp_2, "")
        try:
            result = self.data.cursor().execute("SELECT numEp, nomEp, formeEp, nomDi, nbSportifsEp, dateEp FROM LesEpreuves WHERE categorieEp = ?", [self.ui.comboBox_categorie.currentText()])
        
        except Exception as e:
            self.ui.table_fct_comp_2.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_2, "Impossible d'afficher les résultats : " + repr(e))
        
        else:
            if display.refreshGenericData(self.ui.table_fct_comp_2, result) == 0:
                display.refreshLabel(self.ui.label_fct_comp_2, "Aucun résultat")

    def refreshCatList(self):
        try:
            self.add_range_item(self.ui.comboBox_categorie, ["masculin", "feminin", "mixte"])
        
        except Exception as e:
            self.ui.comboBox_categorie.clear()

    def add_range_item(self, combo, data: list):
        for i in data:
            combo.addItem(i)
