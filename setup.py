from setuptools import setup, find_packages

setup(
    name="support_resistance",
    version="0.0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List your dependencies here
        "pandas>=1.0.0",
        "scipy>=1.0.0",
    ],
)
