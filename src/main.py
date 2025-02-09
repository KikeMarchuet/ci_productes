import sys
import os

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMessageBox, QTableWidgetItem,
    QAbstractItemView, QHeaderView, QWidget, QDialog, QDialogButtonBox,
)
from PySide6.QtUiTools import QUiLoader
from database import Database

class ProductApp(QMainWindow):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        interface1_path = os.path.join(os.path.dirname(__file__), "interface1.ui")
        self.ui = loader.load(interface1_path, None)
        self.db = Database()

        # Configuració del QTableWidget:

        # Amagar la columna ID (columna 0)
        self.ui.tableWidget.setColumnHidden(0, True)

        # Seleccionar tota la fila quan es fa clic
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Deshabilitar l'edició directa a la taula
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Configurar el redimensionament de les columnes:
        # Indiquem que la columna del nom (columna 1) s'estiri per omplir l'espai
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        # I que les columnes de preu (columna 2) i quantitat (columna 3)
        # es redimensionin en funció del seu contingut
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        self.load_products()

        # Assignació dels botons i esdeveniments
        self.ui.btnAfegir.clicked.connect(self.add_product)
        self.ui.btnModificar.clicked.connect(self.update_product)
        self.ui.btnEliminar.clicked.connect(self.delete_product)
        self.ui.tableWidget.itemSelectionChanged.connect(self.load_selected_product)

        self.ui.show()

    def load_products(self):
        """Carrega els productes a la taula."""
        self.ui.tableWidget.setRowCount(0)
        products = self.db.get_all_products()

        for row_index, product in enumerate(products):
            self.ui.tableWidget.insertRow(row_index)
            for col_index, data in enumerate(product):
                self.ui.tableWidget.setItem(row_index, col_index, QTableWidgetItem(str(data)))

    def add_product(self):
        """Afegeix un nou producte."""

        # Cride ara amb el exec per ser un Dialeg
        nova_finestra = FormApp()
        resposta = nova_finestra.exec()

        # Arreplegue resposta de si la decissió es afegir producte i no pulsa Cancelar
        if resposta == QDialog.Accepted:

            # Tot igual però amb els valors de la finestra dialeg
            nom = nova_finestra.ui.txtNom.text()
            preu = nova_finestra.ui.txtPreu.value()
            quantitat = nova_finestra.ui.txtQuantitat.value()

            if nom and preu and quantitat:
                self.db.add_product(nom, preu, quantitat)
                self.load_products()
                # self.clear_inputs()  ---------- > No necessitem netejar camps
            else:
                QMessageBox.warning(self, "Error", "Tots els camps són obligatoris")

    def update_product(self):
        """Modifica el producte seleccionat."""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un producte per modificar")
            return

        # Arreplegue els valors de la fila seleccionada
        product_id = int(self.ui.tableWidget.item(selected_row, 0).text())
        nom_guardat = self.ui.tableWidget.item(selected_row, 1).text()
        preu_guardat = float(self.ui.tableWidget.item(selected_row, 2).text())
        quantitat_guardat = int(self.ui.tableWidget.item(selected_row, 3).text())

        nova_finestra = FormApp()

        # Carregue els valors en dialeg
        nova_finestra.ui.txtNom.setText(nom_guardat)
        nova_finestra.ui.txtPreu.setValue(preu_guardat)
        nova_finestra.ui.txtQuantitat.setValue(quantitat_guardat)

        resposta = nova_finestra.exec()

        # Venim de un dialeg on havem donat al OK
        if resposta == QDialog.Accepted:

            # Missatge de confirmació de si realment modifiquem
            resposta2 = QMessageBox.question(self,"Modificar", 
            "Segur que modifiquem el registre?")

            # Si accepta, fem el canvi
            if resposta2 == QMessageBox.Yes:

                # Update igual però amb els valors de la finestra dialeg
                nom = nova_finestra.ui.txtNom.text()
                preu = nova_finestra.ui.txtPreu.value()
                quantitat = nova_finestra.ui.txtQuantitat.value()

                if nom and preu and quantitat:
                    self.db.update_product(product_id, nom, preu, quantitat)
                    self.load_products()
                    # self.clear_inputs()  ---------- > No necessitem netejar camps
                else:
                    QMessageBox.warning(self, "Error", "Tots els camps són obligatoris")

    def delete_product(self):
        """Elimina el producte seleccionat."""
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Error", "Selecciona un producte per eliminar")
            return

        product_id = int(self.ui.tableWidget.item(selected_row, 0).text())

        # Missatge de confirmació de si realment borrem
        resposta = QMessageBox.question(self,"Borrar", 
            "Segur que borrem el registre?")

        # Si es vol borrar, procedim
        if resposta == QMessageBox.Yes:
            self.db.delete_product(product_id)
            self.load_products()
            # self.clear_inputs()  ---------- > No necessitem netejar camps

    def load_selected_product(self):
        """Carrega les dades del producte seleccionat als camps d’entrada."""
        selected_row = self.ui.tableWidget.currentRow()

        # Açò ho eliminem perquè ja no carreguem al formulari principal
        '''
        if selected_row != -1:
            self.ui.txtNom.setText(self.ui.tableWidget.item(selected_row, 1).text())
            self.ui.txtPreu.setText(self.ui.tableWidget.item(selected_row, 2).text())
            self.ui.txtQuantitat.setText(self.ui.tableWidget.item(selected_row, 3).text())
        '''

    # Tampoc necessitarem netejar camps perquè eixos camps estan al altre formulari i
    # la gestió del contingut la farem des de add_product i update_product
    '''
    def clear_inputs(self):
        """Buida els camps d’entrada."""
        self.ui.txtNom.clear()
        self.ui.txtPreu.clear()
        self.ui.txtQuantitat.clear()
    '''

class FormApp(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        loader = QUiLoader()
        interface2_path = os.path.join(os.path.dirname(__file__), "interface2.ui")
        self.ui = loader.load(interface2_path)

        # El quadre en blanc era perquè em faltava asociar el Layout
        self.setLayout(self.ui.layout())

        # Botons de aceptar i cancel.lar
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductApp()
    sys.exit(app.exec())
