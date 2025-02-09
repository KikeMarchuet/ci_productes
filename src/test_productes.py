import pytest
import sys
from PySide6.QtWidgets import QApplication
from main import ProductApp, FormApp
from database import Database
from PySide6.QtCore import Qt

def app(qtbot):
    """ Segons especificació en https://pytest-qt.readthedocs.io/en/latest/intro.html """
    test_app = ProductApp()
    qtbot.addWidget(test_app.ui)
    return test_app

def test_afegir_producte(qtbot):
    """ Test per comprovar que es pot afegir un producte """
    finestra = ProductApp()
    qtbot.addWidget(finestra)

    # Guardem el numero de productes que tenim
    productes_inicials = len(finestra.db.get_all_products())
    # Estos son els valors de prova
    nom_prova = "Producte Prova"
    preu_prova = 15.50
    quantitat_prova = 3

    # Afegim el registre
    finestra.db.add_product(nom_prova,preu_prova, quantitat_prova)

    # Recarreguem
    finestra.load_products()

    # Comprovem quants tenim ara
    productes_finals = len(finestra.db.get_all_products())
    # Mirem si s'ha incrementat en un, primera pista
    assert productes_finals == productes_inicials + 1

    # Agafem els nous valors de la taula, fijant-nos en el ultim element afegit
    nom_final = finestra.ui.tableWidget.item(productes_finals-1, 1).text()
    preu_final = float(finestra.ui.tableWidget.item(productes_finals-1, 2).text())
    quantitat_final = int(finestra.ui.tableWidget.item(productes_finals-1, 3).text())

    # Comprovem que es correspon amb els valors de prova, segona pista
    assert nom_final == nom_prova
    assert preu_final == preu_prova
    assert quantitat_final == quantitat_prova

def test_modificar_producte(qtbot):
    """ Test per comprovar que es pot modificar un producte """
    finestra = ProductApp()
    qtbot.addWidget(finestra)

    # Vegem que hi haja algun producte
    productes_inicials = len(finestra.db.get_all_products())

    if productes_inicials > 0:

        # Agafem el primer registre
        finestra.ui.tableWidget.selectRow(0)

        # Guardem valors inicials d'eixe registre
        product_id = int(finestra.ui.tableWidget.item(0, 0).text())
        nom_inicial = finestra.ui.tableWidget.item(0, 1).text()
        preu_inicial = float(finestra.ui.tableWidget.item(0, 2).text())
        quantitat_inicial = int(finestra.ui.tableWidget.item(0, 3).text())

        # Modifique eixos valors inicials, afegint "_prova" al nom i incrementant preu i quantitat en un
        finestra.db.update_product(product_id,nom_inicial + "_prova",preu_inicial + 1, quantitat_inicial + 1)

        # Recarreguem
        finestra.load_products()

        # Agafem el primer registre altra vegada
        finestra.ui.tableWidget.selectRow(0)

        # Agafem els nous valors d'eixe registre
        nom_final = finestra.ui.tableWidget.item(0, 1).text()
        preu_final = float(finestra.ui.tableWidget.item(0, 2).text())
        quantitat_final = int(finestra.ui.tableWidget.item(0, 3).text())

        # Mirem si s'ha produit canvi en tots els camps
        assert nom_inicial != nom_final
        assert preu_inicial != preu_final
        assert quantitat_inicial != quantitat_final

def test_eliminar_producte(qtbot):
    """ Test per comprovar que es pot eliminar un producte """
    finestra = ProductApp()
    qtbot.addWidget(finestra)

    # Guardem el numero de productes que tenim
    productes_inicials = len(finestra.db.get_all_products())
    if productes_inicials > 0:
        # Apuntem al primer producte
        product_id = finestra.db.get_all_products()[0][0]
        # Borrem producte
        finestra.db.delete_product(product_id)

        # Comprovem quants queden
        productes_finals = len(finestra.db.get_all_products())
        # Mirem si s'ha reduit en un
        assert productes_finals == productes_inicials - 1


