import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bnlearn2py",
    version="0.0.1",
    author="Pedro V. B. Jeronymo",
    author_email="pedrovbj@gmail.com",
    description="Converts bnlearn.com RDS models to pgmpy models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pedrovbj/bnlearn2py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)