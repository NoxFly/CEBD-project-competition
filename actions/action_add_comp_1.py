import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


class AppAddFct1(QDialog):
    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_add_1.ui", self)

        # selects data
        self.data = data
        self.discipline = ""
        self.epreuve = ""
        self.pays = ""
        self.forme = ""
        self.categorie = ""
        self.numEp = ""
        self.competitor = ""

        # for general loop states simplified (see self.enableComboBox method)
        self.comboBoxes = {
            'discipline': self.ui.Discipline_combo,
            'epreuve': self.ui.Epreuve_combo,
            'pays': self.ui.Pays_combo,
            'forme': self.ui.Forme_combo,
            'categorie': self.ui.Categorie_combo,
            'equipe': self.ui.Equipe_combo
        }

        # refresh & update
        self.refreshDiscipline()
        self.update_country()

        # comboBox event listeners
        self.ui.Discipline_combo.currentTextChanged.connect(self.choose_discipline)
        self.ui.Epreuve_combo.currentTextChanged.connect(self.choose_epreuve)
        self.ui.Pays_combo.currentTextChanged.connect(self.choose_country)
        self.ui.Forme_combo.currentTextChanged.connect(self.choose_forme)
        self.ui.Categorie_combo.currentTextChanged.connect(self.choose_categorie)
        self.ui.Equipe_combo.currentTextChanged.connect(self.choose_competitor)
        self.ui.inscription_button.clicked.connect(self.inscription)

    # Fonction de mise à jour des catégories
    @pyqtSlot()
    def refreshDiscipline(self):
        try:
            result = self.data.cursor().execute("SELECT nomDi FROM LesDisciplines")
            self.enableComboBox(['epreuve', 'pays', 'pays', 'forme', 'categorie', 'equipe'], False)

        except Exception as e:
            print(e)
            display.refreshLabel(self.ui.print_label, "Erreur dans la recherche des Disciplines")

        else:
            self.ui.Discipline_combo.clear()
            self.ui.Discipline_combo.addItem("Choisir une discipline")
            self.add_range_item(self.ui.Discipline_combo, result.fetchall())

    def enableComboBox(self, comboBoxList:list, state:bool):
        for box in comboBoxList:
            if box in self.comboBoxes:
                self.comboBoxes[box].setEnabled(state)

    # Affiche les pays dans le select
    def update_country(self):
        try:
            result = self.data.cursor().execute("SELECT DISTINCT pays from LesSportifs")
        except Exception as e:
            print(e)
            display.refreshLabel(self.ui.print_label, f"Erreur dans la recherche des pays")
        else:
            self.ui.Pays_combo.clear()
            self.ui.Pays_combo.addItem("Choisir un pays")
            self.add_range_item(self.ui.Pays_combo, result)

    # Choose a country
    def choose_country(self, value):
        # no country selected
        if value == "Choisir un pays":
            self.pays = ""
            if self.choose_all():
                self.choose_categorie(self.categorie)

        # specific country selected
        else:
            self.pays = value

            if self.choose_all():
                self.choose_categorie(self.categorie)

    # choose a discipline
    def choose_discipline(self, value):
        if self.discipline != "":
            self.ui.Epreuve_combo.clear()
            self.ui.Forme_combo.clear()
            self.ui.Categorie_combo.clear()
            self.ui.Equipe_combo.clear()
            self.epreuve = ""
            self.forme = ""
            self.categorie = ""
            self.equipe = ""

        # no discipline selected
        if value == "Choisir une discipline":
            self.discipline = ""
            self.enableComboBox(['epreuve', 'forme', 'categorie', 'pays', 'equipe'], False)
            return

        try:
            result = self.data.cursor().execute("SELECT DISTINCT nomEp FROM LesEpreuves WHERE nomDi = ?", [value])
        except Exception as e:
            print(e)
            display.refreshLabel(self.ui.print_label, "Erreur dans la recherche des épreuves")
            self.enableComboBox(['epreuve', 'pays', 'forme', 'categorie', 'equipe'], False)
        else:
            rows = result.fetchall()

            if not rows:
                display.refreshLabel(self.ui.print_label, f"Aucune épreuve associée à la discipline {value}")
                self.enableComboBox(['epreuve', 'pays', 'forme', 'categorie', 'equipe'], False)

            else:                
                display.refreshLabel(self.ui.print_label, "")
                self.ui.Epreuve_combo.clear()
                self.ui.Epreuve_combo.addItem("Choisir une épreuve")
                self.add_range_item(self.ui.Epreuve_combo, rows)
                self.discipline = value
                self.enableComboBox(['epreuve'], True)
                self.enableComboBox(['pays', 'forme', 'categorie', 'equipe'], False)

    # choose a test
    def choose_epreuve(self, value):
        if self.epreuve != "":
            self.ui.Forme_combo.clear()
            self.ui.Categorie_combo.clear()
            self.ui.Equipe_combo.clear()
            self.forme = ""
            self.categorie = ""
            self.equipe = ""

        # no test selected
        if value == "Choisir une épreuve":
            self.epreuve = ""
            self.enableComboBox(['forme', 'categorie', 'pays', 'equipe'], False)
            return

        try:
            result = self.data.cursor().execute("SELECT distinct formeEp from LesEpreuves where nomEp = ?", [value])
        except Exception as e:
            print(e)
            display.refreshLabel(self.ui.print_label, f"Erreur dans la recherche des formes d'épreuve")
            self.enableComboBox(['forme', 'pays', 'categorie', 'equipe'], False)
        else:
            display.refreshLabel(self.ui.print_label, "")
            self.ui.Forme_combo.clear()
            self.ui.Forme_combo.addItem("Choisir une forme")
            self.add_range_item(self.ui.Forme_combo, result)
            self.epreuve = value
            self.enableComboBox(['forme'], True)
            self.enableComboBox(['pays', 'categorie', 'equipe'], False)

    def choose_forme(self, value):
        if self.forme != "":
            self.ui.Categorie_combo.clear()
            self.ui.Equipe_combo.clear()
            self.categorie = ""
            self.equipe = ""

        if value == "Choisir une forme":
            self.forme = ""
            self.enableComboBox(['categorie', 'pays', 'equipe'], False)
            return

        try:
            result = self.data.cursor().execute("SELECT categorieEp FROM LesEpreuves WHERE nomEp = ? AND formeEp = ?", [self.epreuve, value])
        except Exception as e:
            print(e)
            display.refreshLabel(self.ui.print_label, f"Erreur dans la recherche des catégories")
            self.enableComboBox(['categorie', 'pays', 'equipe'], False)
        else:
            self.ui.Categorie_combo.clear()
            self.ui.Categorie_combo.addItem("Choisir une catégorie")
            self.add_range_item(self.ui.Categorie_combo, result)
            self.forme = value
            self.enableComboBox(['categorie'], True)
            self.enableComboBox(['pays', 'equipe'], False)

    # choose a category
    def choose_categorie(self, value):
        if self.categorie != "":
            self.ui.Equipe_combo.clear()
            self.equipe = ""

        if value == "Choisir une catégorie":
            self.categorie = ""
            self.enableComboBox(['equipe'], False)
            return

        try:
            result = self.data.cursor().execute("SELECT numEp FROM LesEpreuves WHERE nomEp = ? AND formeEp = ? AND categorieEp = ?", [self.epreuve, self.forme, value])
            rows = result.fetchall()

            if not rows:
                display.refreshLabel(self.ui.print_label, "Aucune épreuve associée")
                self.enableComboBox(['equipe'], False)
                return

            self.numEp, res = rows[0][0], []

            if self.forme == "individuelle":
                add = " " if self.pays == "" else f" pays = '{self.pays}' AND "
                cat = " " if value == "mixte" else f" AND categorieSp = '{value}' "

                req = f"""SELECT nomSp, prenomSp
                FROM LesSportifs
                WHERE{add}numSp NOT IN (
                    SELECT numIn FROM LesInscriptions WHERE numEp = ?
                ){cat}"""

                res = self.data.cursor().execute(req, [self.numEp])

            else :
                add2 = "" if self.forme != "par couple" else " AND nbEquipiersEq = 2"
                header1, add = "", " "

                if self.pays != "":
                    header1, add = """WITH
                    PaysEquipe AS (
                        SELECT numEq, pays
                        FROM LesEquipiers
                        JOIN LesSportifs_base USING(numSp)
                        GROUP BY numEq
                    )""", f""" numEq IN (
                    SELECT numEq FROM PaysEquipe
                    WHERE pays = '{self.pays}'
                    ) AND """

                header2, cat = " ", ""
                add_pays = "" if value == "mixte" or self.pays == "" else f" AND pays = '{self.pays}'"

                if value != "mixte":
                    header2 = f"""{"," if self.pays else "WITH"} sportifsCat AS (
                        SELECT numSp
                        FROM LesSportifs_base
                        WHERE categorieSp = '{value}'
                    ), A AS (
                        SELECT numSp, numEq, pays, categorieSp
                        FROM LesEquipiers
                        INNER JOIN LesSportifs_base
                        USING(numSp)
                        WHERE numSp IN sportifsCat{add_pays}
                    ), Equipecat AS (
                        SELECT numEq, nbEquipiersEq, pays, categorieSp
                        FROM LesEquipes
                        INNER JOIN A
                        USING(numEq)
                        GROUP BY numEq
                        HAVING COUNT(*) = nbEquipiersEq
                    )"""
                    cat = " AND numEq IN (SELECT numEq FROM Equipecat)"

            req = f"""{header1} {header2}
            SELECT numEq FROM LesEquipes
            WHERE{add}numEq NOT IN (
                SELECT numIn FROM LesInscriptions
                WHERE numEp = ?
            ){add2}{cat}"""
            res = self.data.cursor().execute(req, [self.numEp])

        except Exception as e:
            print(e)
            display.refreshLabel(self.ui.print_label, f"Erreur dans la recherche des inscrits")
            self.enableComboBox(['equipe'], False)
        else:
            rows = res.fetchall()
            if not rows:
                display.refreshLabel(self.ui.print_label, "Aucun participant ne peut être ajouté")
                self.enableComboBox(['equipe'], False)
            else:
                display.refreshLabel(self.ui.print_label, "")
                self.ui.Equipe_combo.clear()

                if self.forme == "individuelle":
                    self.ui.Equipe_combo.addItem("Choisir un sportif")
                    self.add_range_sportif(self.ui.Equipe_combo, rows)
                else:
                    self.ui.Equipe_combo.addItem("Choisir une équipe")
                    self.add_range_item(self.ui.Equipe_combo, rows)

                self.categorie = value
                self.enableComboBox(['pays', 'equipe'], True)

    # choose a competitor
    def choose_competitor(self, value):
        if value not in ["", "Choisir un sportif", "Choisir une équipe"]:
            try:
                int(value)
            except ValueError:
                NumSportif = self.data.cursor().execute("SELECT numSp FROM LesSportifs WHERE nomSp = ? AND prenomSp = ?", value.split(" "))
                value = NumSportif.fetchall()[0][0]
            finally:
                self.competitor = value

    def inscription(self):
        if not self.choose_all() and not self.numEp:
            display.refreshLabel(self.ui.print_label, "Tous les selects n'ont pas été renseignés")
        else:
            try:
                result = self.data.cursor().execute("INSERT INTO LesInscriptions(numIn, numEp) VALUES (?, ?)", [self.competitor, self.numEp])
            except Exception as e:
                display.refreshLabel(self.ui.print_label, "Une erreur est survenue lors de l'inscription")
            else:
                self.ui.Epreuve_combo.clear()
                self.ui.Forme_combo.clear()
                self.ui.Categorie_combo.clear()
                self.ui.Equipe_combo.clear()
                self.update_country()
                self.refreshDiscipline()
                self.enableComboBox(['epreuve', 'pays', 'forme', 'categorie', 'equipe'], False)

                display.refreshLabel(self.ui.print_label, "L'inscription a bien été prise en compte")


    def add_range_item(self, combo, data):
        for i in data:
            for j in i:
                combo.addItem(str(i[0]))


    def add_range_sportif(self, combo, data):
        for i in data:
            combo.addItem(" ".join(i))


    def choose_all(self):
        return self.discipline and self.epreuve and self.forme and self.categorie