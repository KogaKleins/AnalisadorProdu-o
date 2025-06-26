from setuptools import setup, find_packages

setup(
    name="analisador-producao",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.3.0",
        "pdfplumber>=0.11.7",
        "numpy>=2.3.0",
    ],
    python_requires=">=3.10",
)
