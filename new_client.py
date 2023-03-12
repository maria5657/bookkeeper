from bookkeeper.view.main_widget import MainWidget
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from PySide6 import QtWidgets
from bookkeeper.utils import read_tree
import sys

exp_repo_sql = SQLiteRepository[Expense]('123.db', Expense)
cat_repo_sql = SQLiteRepository[Category]('123.db', Category)
bud_repo_sql = SQLiteRepository[Budget]('123.db', Budget)

cat_repo_sql.delete_all()

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

Category.create_from_tree(read_tree(cats), cat_repo_sql)

app = QtWidgets.QApplication(sys.argv)
window = MainWidget(exp_repo_sql, cat_repo_sql, bud_repo_sql)
window.show()
app.exec()
