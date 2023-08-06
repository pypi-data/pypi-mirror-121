import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matchtune-sdk",
    version="1.0.1",
    author="Igal Cohen-Hadria",
    author_email="igal@matchtune.com",
    description="A framework library to access MatchTune API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matchtune-sdk/python-sdk",
    keywords=["music", "matchtune", "sdk"],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
