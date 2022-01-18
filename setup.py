import pathlib
from setuptools import setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="curator_migrations",
    version="1.0.0",
    description="Run curator actions as in doctrine migrations",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/groupe-maison-fr/curator-migrations",
    author="Groupe Maison.fr",
    author_email="it-dev@maison.fr",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["curator_migrations"],
    include_package_data=True,
    install_requires=[
        "elasticsearch-curator",
        "dsnparse"
    ],
    extras_require={
        "testing": [
            "pylint"
        ]
    },
    entry_points={
        "console_scripts": [
            "curatorMigrations=curator_migrations.__main__:main",
        ]
    },
)
