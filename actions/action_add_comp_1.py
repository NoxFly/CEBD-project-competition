import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction à compléter 4


class AppAddFct1(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_add_1.ui", self)
        self.data = data
        self.refreshDiscipline()
        self.ui.Discipline_combo.currentTextChanged.connect(
            self.choise_discipline)

    # Fonction de mise à jour des catégories
    @pyqtSlot()
    def refreshDiscipline(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT nomDi FROM LesDisciplines")

        except Exception as e:
            display.refreshLabel(self.ui.print_label, "Erreur dans la recherche des Disciplines")

        else:
            self.ui.Discipline_combo.clear()
            self.ui.Discipline_combo.addItem("Choisir une discipline")
            self.add_range_item(self.ui.Discipline_combo, cursor.fetchall())
            #display.refreshGenericCombo(self.ui.Discipline_combo, result)

    def choise_discipline(self, value):
        print(value)
        if value == "Choisir une discipline":
            return
        try:
            cursor = self.data.cursor()
            print(value)
            result = cursor.execute(
                "SELECT DISTINCT nomEp FROM LesEpreuves WHERE nomDi = ?", [value])
        except Exception as e:
            display.refreshLabel(self.ui.print_label,
                                 "Erreur dans la recherche des Epreuves")
        else:
            print(cursor.fetchall())
            display.refreshGenericCombo(self.ui.Epreuve_combo, result)

    def add_range_item(self, combo, data):
        for i in data:
            for j in i:
                combo.addItem(str(i[0]))
