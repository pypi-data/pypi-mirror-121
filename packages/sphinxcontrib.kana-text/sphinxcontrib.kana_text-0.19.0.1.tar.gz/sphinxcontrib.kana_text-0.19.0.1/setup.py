import sys
from setuptools import setup
import sphinxcontrib.kana_text as kt

sys.path.append('./sphinxcontrib')
sys.path.append('./test')

setup(
    license = kt.__license__,
    author = kt.__author__,
    url = kt.__url__,
)
