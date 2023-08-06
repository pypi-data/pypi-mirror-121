import setuptools

requirements = ['disnake>=2.1.2']

setuptools.setup(
	name='CoffeePaginator',
	version='1.1a',
	author='Sha4ek',
	description='Простой модуль для создания страниц на Disnake',
	url='https://github.com/Sha4ek/CoffeePaginator',
	packages=setuptools.find_packages(),
	install_requires=requirements,
	classifiers=[
		"Programming Language :: Python :: 3.8",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires='>=3.8',
)