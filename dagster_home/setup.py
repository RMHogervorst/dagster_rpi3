from setuptools import find_packages, setup

setup(
    name="work",
    version="0+dev",
    author="Roel",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    packages=["work"],
    install_requires=[
        "dagit==0.14.7",
        "dagster==0.14.7",
        "dagster-dbt==0.14.7",
        "SQLAlchemy==1.4.35"
        ]
)
