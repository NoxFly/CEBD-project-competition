
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 4
class AppFctComp4(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_4.ui", self)
        self.data = data
        self.refreshCatList()
        self.ui.comboBox_fct_4_pays.currentTextChanged.connect(self.on_combobox_changed)

    # Fonction de mise à jour de l'affichage
    def refreshResult(self):
        display.refreshLabel(self.ui.label_fct_comp_4, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT numSp, nomSp, prenomSp, categorieSp, dateNaisSp FROM LesSportifs_base JOIN LesEquipiers USING (numSp) WHERE pays = ? AND numEq=?",
                [self.ui.comboBox_fct_4_pays.currentText(), int(self.ui.comboBox_fct_4_equipe.currentText())]
            )
        except Exception as e:
            self.ui.table_fct_comp_4.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_4, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_comp_4, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_comp_4, "Aucun résultat")

    # Fonction de mise à jour des catégories
    @pyqtSlot()
    def refreshCatList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT pays FROM LesSportifs_base ORDER BY pays")
        except Exception as e:
            self.ui.comboBox_fct_4_pays.clear()
            self.ui.comboBox_fct_4_equipe.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_fct_4_pays, result)

    def on_combobox_changed(self, value):
        # changer le select des numéros d'équipe en fonction du pays sélectionner ici
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT numEq FROM LesEquipiers E JOIN LesSportifs_base S ON E.numSp = S.numSp WHERE S.pays = ? GROUP BY numEq",
                [self.ui.comboBox_fct_4_pays.currentText()]
            )

            rows = cursor.fetchall()
        except Exception as e:
            self.ui.table_fct_comp_4.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_4, f"Impossible de charger les équipe du pays {value} : {repr(e)}")
        else:
            self.ui.comboBox_fct_4_equipe.clear()
            for row in rows:
                for numEq in row:
                    self.ui.comboBox_fct_4_equipe.addItem(str(numEq))