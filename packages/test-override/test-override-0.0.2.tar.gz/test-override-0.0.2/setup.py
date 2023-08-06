import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='test-override',
    version='0.0.2',
    packages=['test_override'],
    description='Test override',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Linets Development Team',
    author_email='cxasper23@gmail.com',
    url='',
    license='MIT',
    python_requires=">=3.7",
    install_requires=[]
)
