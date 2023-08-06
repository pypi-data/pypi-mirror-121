from setuptools import setup, find_packages, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="delphi4py",
    version="1.0.1",
    author="Pedro B.P.S. Reis",
    author_email="preis@fc.ul.pt",
    description="A python wrapper for the Poisson-Boltzmann Equation solver DelPhi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pedrishi/delphi4py",
    packages=["delphi4py"],
    package_dir={"delphi4py": "delphi4py"},
    package_data={
        "delphi4py": ["readFiles/readFiles.*.so", "rundelphi/rundelphi.*.so"]
    },
)