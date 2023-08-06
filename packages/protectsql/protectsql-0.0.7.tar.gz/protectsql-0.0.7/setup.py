from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='protectsql',
    version='0.0.7',
    author="Arpan Abhishek",
    author_email="arpanforbusiness@gmail.com",
    description="A small package to track SQL injection in flask app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/arpancodes/protectsql",
    project_urls={
        "Bug Tracker": "https://github.com/arpancodes/protectsql/issues",
    },
    install_requires=[
        "Click",
        "Flask",
        "Pyre-check"
    ],
    py_modules=['protectsql'],
    package_dir={"": "."},
    packages=find_packages(where="."),
    entry_points={
        'console_scripts': [
            'protectsql = protectsql.commands:protectsql',
        ],
    },
)
