from setuptools import setup, find_packages

setup(
    name="cinema-frontend",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "requests",
        "streamlit-sortables==0.3.1",
        "pytest>=7.0.0",
        "pytest-mock>=3.10.0"
    ]
)