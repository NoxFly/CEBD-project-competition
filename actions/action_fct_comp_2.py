
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
        # TODO 1.5 : fonction à modifier pour remplacer la zone de saisie par une liste de valeurs prédéfinies dans l'interface une fois le fichier ui correspondant mis à jour
        display.refreshLabel(self.ui.label_fct_comp_2, "")
        """ if not self.ui.lineEdit_fct_comp_2.text().strip():
            self.ui.table_fct_comp_2.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_2,
                                 "Veuillez indiquer un nom de catégorie")
        else:
            try:
                cursor = self.data.cursor()
                result = cursor.execute(
                    "SELECT numEp, nomEp, formeEp, nomDi, nbSportifsEp, dateEp FROM LesEpreuves WHERE categorieSp = ?",
                    [self.ui.lineEdit_fct_comp_2.text().strip()])
            except Exception as e:
                self.ui.table_fct_comp_2.setRowCount(0)
                display.refreshLabel(
                    self.ui.label_fct_comp_2, "Impossible d'afficher les résultats : " + repr(e))
            else:
                i = display.refreshGenericData(
                    self.ui.table_fct_comp_2, result)
                if i == 0:
                    display.refreshLabel(
                        self.ui.label_fct_comp_2, "Aucun résultat") """
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT numEp, nomEp, formeEp, nomDi, nbSportifsEp, dateEp FROM LesEpreuves WHERE categorieEp = ?",
                                    [self.ui.comboBox_categorie.currentText()])
        except Exception as e:
            self.ui.table_fct_comp_2.setRowCount(0)
            display.refreshLabel(
                self.ui.label_fct_comp_2, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(
                self.ui.table_fct_comp_2, result)
            if i == 0:
                display.refreshLabel(
                    self.ui.label_fct_comp_2, "Aucun résultat")

    def refreshCatList(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT categorieEp FROM LesEpreuves")
        except Exception as e:
            self.ui.comboBox_categorie.clear()
        else:
            display.refreshGenericCombo(self.ui.comboBox_categorie, result)
