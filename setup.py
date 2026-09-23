from setuptools import setup, find_packages

setup(
    name="bigdata-architecture-ea4",
    version="1.0.0",
    description="EA4: Documentacion de la Arquitectura y Modelo de Datos - Proyecto Integrador Big Data",
    author="IU Digital de Antioquia - Estudiante",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "pandas>=2.2.0",
        "openpyxl>=3.1.2",
        "numpy>=1.26.0",
        "scikit-learn>=1.4.0",
        "matplotlib>=3.8.0",
        "reportlab>=4.0.0",
        "Pillow>=10.0.0",
    ],
    python_requires=">=3.9",
)
