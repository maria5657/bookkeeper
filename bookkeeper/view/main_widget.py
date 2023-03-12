"""
This is Main Widget
"""
from PySide6 import QtWidgets
from bookkeeper.view.uadc_table import UADCTable
from bookkeeper.view.analytical_table import AnalyticalTable
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


class MainWidget(QtWidgets.QWidget):
    """
    Main Widget
    """

    def __init__(  # type: ignore[no-untyped-def]
            self,
            exp_bd: AbstractRepository[Expense],
            cat_bd: AbstractRepository[Category],
            budg_bd: AbstractRepository[Budget], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.setWindowTitle('The Bookkeeper App')
        self.layout = QtWidgets.QVBoxLayout()  # type: ignore[assignment]
        #  expanses table
        self.table1 = UADCTable(exp_bd, 'Таблица расходов')
        self.layout.addWidget(self.table1)  # type: ignore[attr-defined]
        #  categories table
        self.table2 = UADCTable(cat_bd, 'Таблица категорий')
        self.layout.addWidget(self.table2)  # type: ignore[attr-defined]
        #  budget table
        self.table3 = AnalyticalTable(budg_bd, exp_bd, 'Таблица бюджетов')
        self.layout.addWidget(self.table3)  # type: ignore[attr-defined]
        self.setLayout(self.layout)  # type: ignore[arg-type]
