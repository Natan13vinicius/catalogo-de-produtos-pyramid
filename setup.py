from setuptools import setup

setup(
    name="mycatalog",
    version="0.1.0",
    packages=["mycatalog"],
    include_package_data=True,
    install_requires=[
        "pyramid>=2.0",
        "pyramid-jinja2",
        "SQLAlchemy>=2.0",
        "waitress",
    ],
    entry_points={
        "paste.app_factory": [
            "main = mycatalog:main",
        ],
    },
)
