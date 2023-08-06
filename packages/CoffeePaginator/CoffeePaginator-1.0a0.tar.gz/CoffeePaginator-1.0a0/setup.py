import setuptools

requirements = ["disnake>=2.1.2"]

setuptools.setup(
	# Имя дистрибутива пакета. Оно должно быть уникальным, поэтому добавление вашего имени пользователя в конце является обычным делом.
	name="CoffeePaginator",
	# Номер версии вашего пакета. Обычно используется семантическое управление версиями.
	version="1.0a",
	# Имя автора.
	author="Sha4ek",
	# Краткое описание, которое будет показано на странице PyPi.
	description="Простой модуль для создания страниц в Disnake",
	# URL-адрес, представляющий домашнюю страницу проекта. Большинство проектов ссылаются на репозиторий.
	url="https://github.com/Sha4ek/CoffeePaginator",
	# Находит все пакеты внутри проекта и объединяет их в дистрибутив.
	packages=setuptools.find_packages(),
	# Предоставляет pip некоторые метаданные о пакете. Также отображается на странице PyPi.
	install_requires=requirements,

	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	# Требуемая версия Python.
	python_requires='>=3.8',
)