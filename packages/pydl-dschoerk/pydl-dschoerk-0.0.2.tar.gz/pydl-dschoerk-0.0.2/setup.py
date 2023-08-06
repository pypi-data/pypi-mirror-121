import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydl-dschoerk",
    version="0.0.2",
    author="Dominik Schörkhuber",
    author_email="dschoerk@gmx.at",
    description="Simple file downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dschoerk/pydl",
    project_urls={
        
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
          'wget',
      ],
)