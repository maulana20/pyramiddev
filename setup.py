from setuptools import setup

requires = [
	'deform',
	'pyramid',
	'pyramid_chameleon',
	'waitress',
	'pyramid_tm',
	'sqlalchemy',
	'zope.sqlalchemy',
]

dev_requires = [
	'pyramid_debugtoolbar',
	'pytest',
	'webtest',
]

setup(
	name='pyramiddev',
	install_requires=requires,
	extras_require={
		'dev': dev_requires,
	},
	entry_points={
		'paste.app_factory': [
			'main = pyramiddev:main'
		],
		'console_scripts': [
			'initialize_pyramiddev_db = pyramiddev.initialize_db:main'
		],
	},
)
