import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nimbbl-python-sdk",
    version="0.0.3",
    author="Rakshit",
    author_email="rakshit@nimbbl.biz",
    description="Nimbbl SDK for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nimbbl-tech/nimbbl-python-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/nimbbl-tech/nimbbl-python-sdk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    include_package_data=True,
    packages=setuptools.find_packages("src"),
    python_requires=">=3.6",
)