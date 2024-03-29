from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'pyramid',
    'pyramid_chameleon',
    'sqlalchemy',
    'zope.sqlalchemy',
    'psycopg2',
    'waitress',
    'webtest',
    'transaction',
    'Paste',
]
# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.
dev_requires = [
    'pyramid_debugtoolbar',
    'pytest',
    'apache-log-parser',
]


setup(
    name='dummy_app',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
     'paste.app_factory': [
        'main = dummy_app:main'
     ],
     'console_scripts': [
        'create_logger = logger.create_logger:main'
     ],
    },
)
