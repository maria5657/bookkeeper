"""
Analytical Table
"""
from PySide6 import QtWidgets
from bookkeeper.view.uadc_table import UADCTable
from bookkeeper.repository.abstract_repository import AbstractRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.expense import Expense


class AnalyticalTable(QtWidgets.QWidget):
    """
    Brilliant analytical table
    """

    def __init__(  # type: ignore[no-untyped-def]
            self,
            area_repo: AbstractRepository[Budget],
            study_repo: AbstractRepository[Expense],
            tname: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.study_repo = study_repo
        self.area_repo = area_repo
        self.layout = QtWidgets.QVBoxLayout()  # type: ignore[assignment]
        #  budget table
        self.table = UADCTable(area_repo, tname)
        self.layout.addWidget(self.table)  # type: ignore[attr-defined]
        #  update calculations button
        calculate_button = QtWidgets.QPushButton('Пересчитать бюджет')
        self.layout.addWidget(calculate_button)  # type: ignore[attr-defined]
        calculate_button.clicked.connect(self.calc_budg)  # type: ignore[attr-defined]
        self.setLayout(self.layout)  # type: ignore[arg-type]

    def calc_budg(self) -> None:
        """
        Norm function, kinda like it
        """
        data = self.study_repo.get_all()
        for period in self.area_repo.get_all():
            cur_val = period
            cur_val.value = period.calculate(data)
            self.area_repo.update(cur_val)
        self.table.refresh_click()
