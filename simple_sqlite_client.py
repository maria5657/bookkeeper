"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree


cat_repo_sql = SQLiteRepository[Category]('123.db', Category)
exp_repo_sql = SQLiteRepository[Expense]('123.db', Expense)

cat_repo_sql.delete_all()
exp_repo_sql.delete_all()

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

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'cats':
        print(*cat_repo_sql.get_all(), sep='\n')
    elif cmd == 'exps':
        print(*exp_repo_sql.get_all(), sep='\n')
    elif cmd == 'delete expanse':
        print(*exp_repo_sql.get_all(), sep='\n')
        cmd1 = int(input('введите id записи для удаления $> '))
        exp_repo_sql.delete(cmd1)

    elif cmd == 'delete category':
        print(*cat_repo_sql.get_all(), sep='\n')
        cmd1 = int(input('введите id записи для удаления $> '))
        cat_repo_sql.delete(cmd1)
    
    elif cmd == 'about cat':
        print(*cat_repo_sql.get_all(), sep='\n')
        cmd1 = int(input('введите id записи для получения информации $> '))
        print(cat_repo_sql.get(cmd1))

    elif cmd == 'about exp':
        print(*exp_repo_sql.get_all(), sep='\n')
        cmd1 = int(input('введите id записи для получения информации $> '))
        print(exp_repo_sql.get(cmd1))

    elif cmd == 'update exp':
        print(*exp_repo_sql.get_all(), sep='\n')
        cmd1 = int(input('введите id записи для обновления $> '))
        print(exp_repo_sql.get(cmd1))
        cmd2 = input('введите новую запись $> ')
        amount, *name = cmd2.split(' ')
        try:
            cat = cat_repo_sql.get_all({'name': ' '.join(name)})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.name, cmd1)
        exp_repo_sql.update(exp)

    elif cmd == 'update cat':
        print(*cat_repo_sql.get_all(), sep='\n')
        cmd1 = int(input('введите id записи для обновления $> '))
        print(cat_repo_sql.get(cmd1))
        cmd2 = input('введите новую запись $> ')
        *name, parent = cmd2.split()
        if parent == 'None' or parent == 'none':
            parent = None
        cat = Category(' '.join(name), parent, cmd1)
        cat_repo_sql.update(cat)

    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo_sql.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.name)
        exp_repo_sql.add(exp)
