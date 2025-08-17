from setuptools import setup

setup(
    name='BankFund',
    version='1.0.0',
    author='Berk Acunaş',
    author_email='berk@deponessoft.com',
    description='BankFund module',
    packages=['bankfund', 'bankfund/entities', 'bankfund/entities/sqlite', 'bankfund/entities/sqlserver', 'bankfund/entities/textserver'],
    install_requires=['requests', 'lxml', 'beautifulsoup4', 'pymssql', 'db-sqlite3', 'julian', 'pandas', 'numpy', 'xlsxwriter', 'html5lib', 'matplotlib', 'sqlalchemy', 'setuptools']
)