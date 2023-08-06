from setuptools import setup, find_packages

setup(
    name="testpackages32",
    version="0.2.3",
    author="Igor Simagin",
    author_email="igorsim35@gmail.com",
    install_requires=[
        "numpy",
        "pandas"
    ],
    include_package_data=True,
    packages=find_packages(),
)