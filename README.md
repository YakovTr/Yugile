# FinanceBot
### FinanceBot - это бот для контроля финансов, который поможет вам отслеживать свои расходы и доходы
## Установка
1. Скопируйте код бота из файла main.py.
2. Установите необходимые библиотеки, выполнив команду pip install -r requirements.txt.
3. Создайте файл config.py и укажите в нем токен вашего бота, получив его у BotFather.
4. Запустите бота, выполнив команду python main.py.
## Команды
- /start - начать работу с ботом
- /add_expense - добавить расход
- /add_income - добавить доход
- /view_balance - посмотреть баланс
- /view_expenses - посмотреть расходы по категориям
- /view_incomes - посмотреть доходы по категориям
- /help - вывести список команд
## Использование
- Чтобы добавить расход или доход, отправьте боту сообщение в формате /add_expense <сумма> <категория> или /add_income <сумма> <категория>, где <сумма> - это сумма расхода или дохода, а <категория> - это категория расхода или дохода. Например:


- - /add_expense 100 еда
- - /add_income 5000 зарплата
- Чтобы посмотреть баланс, расходы по категориям или доходы по категориям, отправьте боту соответствующую команду:


- - /view_balance
- - /view_expenses
- - /view_incomes
- Чтобы посмотреть список команд, отправьте боту команду /help.
- Чтобы обновить данные и сбросить все доходы и расходы введите /reset

## База данных
### Бот использует базу данных SQLite для хранения информации о пользователях, расходах и доходах. База данных содержит три таблицы:

- users - таблица пользователей, содержащая столбцы user_id и username
- expenses - таблица расходов, содержащая столбцы id, user_id, amount и category
- income - таблица доходов, содержащая столбцы id, user_id, amount и category
- При первом запуске бота будут созданы все необходимые таблицы.