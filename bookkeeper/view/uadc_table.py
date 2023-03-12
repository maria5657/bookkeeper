"""
UADC Table stands for UpdateAddDeleteChange Table.
"""

from PySide6 import QtWidgets
from PySide6.QtCore import QDateTime
from bookkeeper.repository.abstract_repository import AbstractRepository


class UADCTable(QtWidgets.QWidget):
    """
    UADC TABLE
    """

    def __init__(  # type: ignore[no-untyped-def]
            self,
            repo: AbstractRepository,  # type: ignore[type-arg]
            tablename: str,
            *args,
            **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.repo = repo
        self.layout = QtWidgets.QGridLayout()  # type: ignore[assignment]

        self.tablename = QtWidgets.QLabel(tablename)
        self.layout.addWidget(self.tablename, 0, 0, 1, 1)  # type: ignore[attr-defined]
        self.btn = QtWidgets.QPushButton('Обновить')
        self.btn.clicked.connect(self.refresh_click)  # type: ignore[attr-defined]
        self.layout.addWidget(self.btn, 0, 1, 1, 1)  # type: ignore[attr-defined]

        self.add_btn = QtWidgets.QPushButton('Добавить')
        self.add_btn.clicked.connect(self.add_menu)  # type: ignore[attr-defined]
        self.layout.addWidget(self.add_btn, 0, 2, 1, 1)  # type: ignore[attr-defined]

        self.delete_btn = QtWidgets.QPushButton('Удалить')
        self.delete_btn.clicked.connect(self.del_menu)  # type: ignore[attr-defined]
        self.layout.addWidget(self.delete_btn, 0, 3, 1, 1)  # type: ignore[attr-defined]

        self.upd_btn = QtWidgets.QPushButton('Исправить')
        self.upd_btn.clicked.connect(self.upd_menu)  # type: ignore[attr-defined]
        self.layout.addWidget(self.upd_btn, 0, 4, 1, 1)  # type: ignore[attr-defined]

        self.exp_tabl = QtWidgets.QTableWidget(
            20,
            len(self.repo.fields) + 1)  # type: ignore[attr-defined]
        for i, element in enumerate(
                self.repo.names.split(',')  # type: ignore[attr-defined]
        ):
            self.exp_tabl.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(element))
        self.exp_tabl.setHorizontalHeaderItem(
            len(self.repo.fields),  # type: ignore[attr-defined]
            QtWidgets.QTableWidgetItem('PK')
        )
        self.layout.addWidget(self.exp_tabl, 1, 0, 1, 50)  # type: ignore[attr-defined]
        self.setLayout(self.layout)  # type: ignore[arg-type]

        self.dlg = QtWidgets.QDialog()
        self.dlg_widgets: list = []  # type: ignore[type-arg]

    def refresh_click(self) -> None:
        """
        refresh
        """
        result = self.repo.get_all()
        to_table = []
        for element in result:
            values = [getattr(element, x)
                      for x in self.repo.fields]  # type: ignore[attr-defined]
            values.append(getattr(element, 'pk'))
            to_table.append(values)
        self.exp_tabl.clearContents()
        self.add_data(to_table)

    def add_menu(self) -> None:
        """
        refresh
        """
        self.dlg = QtWidgets.QDialog()
        layout = QtWidgets.QGridLayout()
        self.dlg_widgets = []
        for i, element in enumerate(self.repo.fields):  # type: ignore[attr-defined]
            if element == 'category':
                self.dlg_widgets.append(QtWidgets.QComboBox())
                self.dlg_widgets[-1].addItem('книги')
                self.dlg_widgets[-1].addItem('мясо')
                self.dlg_widgets[-1].addItem('одежда')
                self.dlg_widgets[-1].addItem('сырое мясо')
                self.dlg_widgets[-1].addItem('сладости')
            elif 'date' in element:
                self.dlg_widgets.append(QtWidgets.QDateTimeEdit())
                self.dlg_widgets[-1].setDateTime(QDateTime.currentDateTime())
            else:
                self.dlg_widgets.append(QtWidgets.QLineEdit())
            layout.addWidget(QtWidgets.QLabel(str(element)), i, 0)
            layout.addWidget(self.dlg_widgets[-1], i, 1)
        add = QtWidgets.QPushButton('Добавить')
        cancel = QtWidgets.QPushButton('Отменить')
        cancel.clicked.connect(self.cancel)  # type: ignore[attr-defined]
        add.clicked.connect(self.add_click)  # type: ignore[attr-defined]
        layout.addWidget(add, len(self.repo.fields) + 1, 0)  # type: ignore[attr-defined]
        layout.addWidget(cancel,
                         len(self.repo.fields) + 1, 1)  # type: ignore[attr-defined]
        self.dlg.setLayout(layout)
        self.dlg.setWindowTitle('Добавить покупку')
        self.dlg.exec()

    def cancel(self) -> None:
        """
        refresh
        """
        self.dlg.close()

    def add_click(self) -> None:
        """
        refresh
        """
        to_table = []
        for element in self.dlg_widgets:
            if isinstance(element, QtWidgets.QDateTimeEdit):
                try:
                    to_table.append(element.dateTime().toPython())
                except AttributeError as e:
                    print(e)
            else:
                try:
                    to_table.append(int(element.text()))
                except AttributeError:
                    to_table.append(element.currentText())
                except ValueError:
                    to_table.append(element.text())
        self.repo.add(self.repo.cls(*to_table))  # type: ignore[attr-defined]
        self.refresh_click()
        self.dlg.close()

    def del_menu(self) -> None:
        """
        refresh
        """
        self.dlg = QtWidgets.QDialog()
        self.dlg_widgets = []
        layout = QtWidgets.QGridLayout()
        self.dlg_widgets.append(QtWidgets.QLabel())
        layout.addWidget(self.dlg_widgets[-1], 0, 0)
        self.dlg_widgets.append(QtWidgets.QLineEdit())
        layout.addWidget(self.dlg_widgets[-1], 0, 1)
        add = QtWidgets.QPushButton('Применить')
        cancel = QtWidgets.QPushButton('Отменить')
        cancel.clicked.connect(self.cancel)  # type: ignore[attr-defined]
        add.clicked.connect(self.del_click)  # type: ignore[attr-defined]
        layout.addWidget(add, 1, 0)
        layout.addWidget(cancel, 1, 1)
        self.dlg.setLayout(layout)
        self.dlg.setWindowTitle('Удалить запись')
        self.dlg.exec()

    def del_click(self) -> None:
        """
        refresh
        """
        try:
            self.repo.delete(int(self.dlg_widgets[-1].text()))
        except Exception as err:
            print('Unable to delete object')
            print(err)
        finally:
            self.refresh_click()
            self.dlg.close()

    def upd_menu(self) -> None:
        """
        refresh
        """
        self.dlg = QtWidgets.QDialog()
        layout = QtWidgets.QGridLayout()
        self.dlg_widgets = []
        for i, element in enumerate(self.repo.fields):  # type: ignore[attr-defined]
            if element == 'category':
                self.dlg_widgets.append(QtWidgets.QComboBox())
                self.dlg_widgets[-1].addItem('книги')
                self.dlg_widgets[-1].addItem('мясо')
                self.dlg_widgets[-1].addItem('одежда')
                self.dlg_widgets[-1].addItem('сырое мясо')
                self.dlg_widgets[-1].addItem('сладости')
            elif 'date' in element:
                self.dlg_widgets.append(QtWidgets.QDateTimeEdit())
                self.dlg_widgets[-1].setDateTime(QDateTime.currentDateTime())
            else:
                self.dlg_widgets.append(QtWidgets.QLineEdit())
            layout.addWidget(QtWidgets.QLabel(str(element)), i, 0)
            layout.addWidget(self.dlg_widgets[-1], i, 1)
        self.dlg_widgets.append(QtWidgets.QLineEdit())
        layout.addWidget(QtWidgets.QLabel('PK'),
                         len(self.repo.fields), 0)  # type: ignore[attr-defined]
        layout.addWidget(self.dlg_widgets[-1],
                         len(self.repo.fields), 1)  # type: ignore[attr-defined]
        add = QtWidgets.QPushButton('Исправить')
        cancel = QtWidgets.QPushButton('Отменить')
        cancel.clicked.connect(self.cancel)  # type: ignore[attr-defined]
        add.clicked.connect(self.upd_click)  # type: ignore[attr-defined]
        layout.addWidget(add, len(self.repo.fields) + 1, 0)  # type: ignore[attr-defined]
        layout.addWidget(cancel,
                         len(self.repo.fields) + 1, 1)  # type: ignore[attr-defined]
        self.dlg.setLayout(layout)
        self.dlg.setWindowTitle('Исправить запись')
        self.dlg.exec()

    def upd_click(self) -> None:
        """
        refresh
        """
        to_table = []
        for element in self.dlg_widgets:
            if isinstance(element, QtWidgets.QDateTimeEdit):
                try:
                    to_table.append(element.dateTime().toPython())
                except AttributeError as err:
                    print(err)
            else:
                try:
                    to_table.append(int(element.text()))
                except AttributeError:
                    to_table.append(element.currentText())
                except ValueError:
                    to_table.append(element.text())
        tmp = self.repo.cls(*to_table)  # type: ignore[attr-defined]
        print(to_table)
        print(tmp)
        self.repo.update(self.repo.cls(*to_table))  # type: ignore[attr-defined]
        self.refresh_click()
        self.dlg.close()

    def add_data(self, data: list) -> None:  # type: ignore[type-arg]
        """
        refresh
        """
        for inum, row in enumerate(data):
            for jnum, x in enumerate(row):
                self.exp_tabl.setItem(
                    inum, jnum,
                    QtWidgets.QTableWidgetItem(str(x))
                )
