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
        self.discipline = ""
        self.epreuve = ""
        self.pays = ""
        self.forme = ""
        self.categorie = ""
        self.numEp = ""
        self.competitor = ""
        self.refreshDiscipline()
        self.update_country()
        self.ui.Discipline_combo.currentTextChanged.connect(self.choise_discipline)
        self.ui.Epreuve_combo.currentTextChanged.connect(self.choise_epreuve)
        self.ui.Pays_combo.currentTextChanged.connect(self.choise_country)
        self.ui.Forme_combo.currentTextChanged.connect(self.choise_forme)
        self.ui.Categorie_combo.currentTextChanged.connect(self.choise_categorie)
        self.ui.Equipe_combo.currentTextChanged.connect(self.choise_competitor)
        self.ui.inscription_button.clicked.connect(self.inscription)

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

    def update_country(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT pays from LesSportifs")
        except Exception as e:
            print(e)
            display.refreshLabel(self.ui.print_label, f"Erreur dans la recherche des pays")
        else:
            #display.refreshGenericCombo(self.ui.Pays_combo,result)
            self.ui.Pays_combo.clear()
            self.ui.Pays_combo.addItem("Choisir un pays")
            self.add_range_item(self.ui.Pays_combo,result)

    def choise_country(self,value):
        if value == "Choisir un pays":
            self.pays = ""
            if self.choise_all():
                self.choise_categorie(self.categorie)
            return
        self.pays = value
        if self.choise_all():
            self.choise_categorie(self.categorie)

    def choise_discipline(self, value):
        if self.discipline != "":
            self.ui.Epreuve_combo.clear()
            self.ui.Forme_combo.clear()
            self.ui.Categorie_combo.clear()
            self.ui.Equipe_combo.clear()
        if value == "Choisir une discipline":
            self.discipline = ""
            return
        try:
            cursor = self.data.cursor()
            result = cursor.execute(
                "SELECT DISTINCT nomEp FROM LesEpreuves WHERE nomDi = ?", [value])
        except Exception as e:
            display.refreshLabel(self.ui.print_label, "Erreur dans la recherche des Epreuves")
        else:
            rows = cursor.fetchall()
            if rows == []:
                #self.ui.Epreuve_combo.hide()
                display.refreshLabel(self.ui.print_label,f"Aucune epreuve associée a la discipline {value}")
                return
            #display.refreshGenericCombo(self.ui.Epreuve_combo, result)
            display.refreshLabel(self.ui.print_label,"")
            self.ui.Epreuve_combo.clear()
            self.ui.Epreuve_combo.addItem("Choisir une epreuve")
            self.add_range_item(self.ui.Epreuve_combo,rows)
            self.discipline = value

    def choise_epreuve(self,value):
        if self.epreuve != "":
            self.ui.Forme_combo.clear()
            self.ui.Categorie_combo.clear()
            self.ui.Equipe_combo.clear()

        if value == "Choisir une epreuve":
            self.epreuve = ""
            return
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT distinct formeEp from LesEpreuves where nomEp = ?",[value])
        except Exception as e:
            print(e)
            display.refreshLabel(self.ui.print_label, f"Erreur dans la recherche des Formes")
        else:
            display.refreshLabel(self.ui.print_label,"")
            self.ui.Forme_combo.clear()
            self.ui.Forme_combo.addItem("Choisir une forme")
            self.add_range_item(self.ui.Forme_combo,result)
            self.epreuve = value

    def choise_forme(self,value):
        if self.forme != "":
            self.ui.Categorie_combo.clear()
            self.ui.Equipe_combo.clear()
        if value == "Choisir une forme":
            self.forme = ""
            return
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT categorieEp FROM LesEpreuves WHERE nomEp = ? AND formeEp = ?",[self.epreuve,value])
        except Exception as e:
            print(e)
            display.refreshLabel(self.ui.print_label, f"Erreur dans la recherche des categories")
        else:
            self.ui.Categorie_combo.clear()
            self.ui.Categorie_combo.addItem("Choisir une catégorie")
            self.add_range_item(self.ui.Categorie_combo,result)
            self.forme = value

    def choise_categorie(self,value):
        print(f"Pays courant : {self.pays}")
        if self.categorie != "":
            self.ui.Equipe_combo.clear()
        if value == "Choisir une catégorie":
            self.categorie = ""
            return
        try:
            cursor = self.data.cursor()
            query = cursor.execute("SELECT numEp FROM LesEpreuves WHERE nomEp = ? AND formeEp = ? AND categorieEp = ?",[self.epreuve,self.forme,value])
            rows = query.fetchall()
            print(f"Valeur de la query : {rows}")
            if rows == []:
                display.refreshLabel(self.ui.print_label,"Aucune épreuve associée")
                return
            self.numEp = rows[0][0]
            result = []
            if self.forme == "individuelle":
                if self.pays != "":
                    add:str = f" pays = '{self.pays}' AND "
                else:
                    add:str = " "
                if value != "mixte":
                    cat:str = f" AND categorieSp = '{value}' "
                else:
                    cat:str = " "
                req = f"""
                SELECT nomSp, prenomSp
                from LesSportifs
                where{add}numSp NOT IN (
                    select numIn from LesInscriptions where numEp = ?
                ){cat}
                """
                result = cursor.execute(req,[self.numEp])
            else :
                if self.pays != "":
                    header1 = """
                    WITH
                    PaysEquipe AS (
                        SELECT numEq, pays
                        FROM LesEquipiers
                        JOIN LesSportifs_base USING (numSp)
                        GROUP BY numEq
                    )"""
                    add:str = f""" numEq IN (
                    select numEq from PaysEquipe
                    where pays = '{self.pays}'
                    ) AND """
                else:
                    add:str = " "
                    header1 = ""
                if self.forme == "par couple":
                    add2:str = " AND nbEquipiersEq = 2"
                else:
                    add2:str = ""
                if value == "mixte":
                    header2:str = " "
                    cat:str = ""
                else:
                    if self.pays != "":
                        add_pays = f" AND pays = '{self.pays}'"
                    else:
                        add_pays = ""
                    header2:str = f"""
                    {"," if self.pays else "WITH "}sportifsCat AS (
                        SELECT numSp
                        FROM LesSportifs_base
                        WHERE categorieSp = '{value}'
                    ), A AS (
                        SELECT numSp, numEq, pays, categorieSp
                        FROM LesEquipiers
                        INNER JOIN LesSportifs_base
                        USING(numSp)
                        WHERE
                            numSp IN sportifsCat{add_pays}
                    ), Equipecat AS(
                        SELECT numEq, nbEquipiersEq, pays, categorieSp
                        FROM LesEquipes
                        INNER JOIN A
                        USING(numEq)
                        GROUP BY numEq
                        HAVING COUNT(*) = nbEquipiersEq
                    )
                    """
                    cat:str = " AND numEq IN (SELECT numEq from Equipecat)"
                req = f"""
                {header1}
                {header2}
                select numEq from LesEquipes
                where{add}numEq NOT IN (
                    select numIn from LesInscriptions
                    where numEp = ?
                ){add2}{cat}
                """
                print(req)
                result = cursor.execute(req,[self.numEp])


        except Exception as e:
            print("probleme")
            print(e)
            display.refreshLabel(self.ui.print_label, f"Erreur dans la recherche des inscrits")
        else:
            rows = result.fetchall()
            if rows == []:
                display.refreshLabel(self.ui.print_label,"Aucun participant ne peut etre ajouté")
                return
            self.ui.Equipe_combo.clear()
            if self.forme == "individuelle" :
                self.ui.Equipe_combo.addItem("Choisir un sportif")
                self.add_range_sportif(self.ui.Equipe_combo,rows)
            else:
                self.ui.Equipe_combo.addItem("Choisir une equipe")
                self.add_range_item(self.ui.Equipe_combo,rows)
            self.categorie = value

    def choise_competitor(self,value):
        print(f"valeur des competiteur : {value}")
        if value in ["", "Choisir un sportif", "Choisir une equipe"]:
            return
        try:
            int(value)
        except ValueError:
            cursor = self.data.cursor()
            NumSportif = cursor.execute("SELECT numSp FROM LesSportifs WHERE nomSp = ? AND prenomSp = ?", value.split(" "))
            res = NumSportif.fetchall()
            value = res[0][0]
        finally:
            print(f"Value at the end : {value}")
            self.competitor = value

    def inscription(self):
        if not self.choise_all() and not self.numEp:
            display.refreshLabel(self.ui.print_label,"Toutes les combo box ne sont pas séléctionnée")
            return
        try:
            cursor = self.data.cursor()
            result = cursor.execute("INSERT INTO LesInscriptions(numIn,numEp) VALUES (?,?)",[self.competitor,self.numEp])
        except Exception as e:
            display.refreshLabel(self.ui.print_label,"Impossible d'ajouter l'inscription")
        else:
            self.ui.Epreuve_combo.clear()
            self.ui.Forme_combo.clear()
            self.ui.Categorie_combo.clear()
            self.ui.Equipe_combo.clear()
            display.refreshLabel(self.ui.print_label,"L'inscription à bien été prise en compte")

    def add_range_item(self, combo, data):
        for i in data:
            for j in i:
                combo.addItem(str(i[0]))

    def add_range_sportif(self,combo,data):
        for i in data:
            combo.addItem(" ".join(i))

    def choise_all(self):
        return self.discipline and self.epreuve and self.forme and self.categorie

    def print_values(self):
        print(f"1 -> {self.discipline}")
        print(f"2 -> {self.epreuve}")
        print(f"3 -> {self.forme}")
        print(f"4 -> {self.categorie}")