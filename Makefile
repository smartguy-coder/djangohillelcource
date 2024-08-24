# Makefile для Django-проєкту

# Команда для запуску manage.py, яку записуємо в змінну
MANAGE = python manage.py

# Запуск розробницького серверу
.PHONY: runserver
runserver:
	$(MANAGE) runserver # тут $(MANAGE) є синтаксисом підстановки раніше створеної змінної, можна порівняти з f-стрічками в пайтоні