import os
from setuptools import setup, find_packages

PACKAGE = "BankFund"
NAME = "BankFund"
DESCRIPTION = "" 
AUTHOR = "Berk Acunaş"
AUTHOR_EMAIL = 'berk@deponessoft.com'
URL = "https://github.com/berkacunas/BankFund"
DOWNLOAD_URL = "https://github.com/berkacunas/BankFund.git"
LICENSE="GPL"
VERSION = "1.0.0"

here = os.path.abspath(os.path.dirname(__file__))

long_description = ""

setup(
    name=NAME,
    version=VERSION,
    url=URL,
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    author=AUTHOR,
    install_requires=['beautifulsoup4>=4.13.4',
                      'db-sqlite3>=0.0.1',
                      'html5lib>=1.1',
                      'julian>=0.14',
                      'lxml>=5.4.0',
                      'matplotlib>=3.10.3',
                      'numpy>=2.3.0',
                      'pandas>=2.3.0',
                      'pymssql>=2.3.4',
                      'requests>=2.32.4',
                      'SQLAlchemy>=2.0.42',
                      'XlsxWriter>=3.2.3'],
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    packages=find_packages(), 
    include_package_data=True,
    platforms='any'
)





# setup(
#     name='BankFund',
#     version='1.0.0',
#     author='Berk Acunaş',
#     author_email='berk@deponessoft.com',
#     description='BankFund module',
#     packages=['bankfund', 
#               'bankfund/contextmanager', 
#               'bankfund/globals',
#               'bankfund/ios',
#               'bankfund/entities', 
#               'bankfund/entities/sqlite', 
#               'bankfund/entities/sqlserver', 
#               'bankfund/entities/textserver'
#               ],
    
#     install_requires=['requests', 'lxml', 'beautifulsoup4', 'pymssql', 'db-sqlite3', 'julian', 'pandas', 'numpy', 'xlsxwriter', 'html5lib', 'matplotlib', 'sqlalchemy', 'setuptools']
# )