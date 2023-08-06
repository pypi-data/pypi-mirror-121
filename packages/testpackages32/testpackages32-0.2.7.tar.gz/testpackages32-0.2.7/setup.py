from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="testpackages32",
    version="0.2.7",
    author="Igor Simagin",
    author_email="igorsim35@gmail.com",
    install_requires=[
        "numpy",
        "pandas"
    ],
    long_description=long_description,
    description="lulw",
    long_description_content_type='text/markdown',
    include_package_data=True,
    packages=find_packages(),
)

# python setup.py sdist bdist_wheel
# twine upload dist/*