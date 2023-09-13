from setuptools import setup, find_packages

setup(
    name="support_resistance",
    version="0.0.3",
    packages=find_packages(),
    description='Lib for finding support resistance levels',
    author='Alexander Pantyukhin',
    author_email='apantykhin@gmail.com',
    install_requires=[
        "pandas>=1.0.0",
        "scipy>=1.0.0",
    ],
)
