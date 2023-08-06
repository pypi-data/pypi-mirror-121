import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dirlist",
    version="0.0.0",
    author="Fasm.ga",
    author_email="developers@fasmga.org",
    description="A directory listing server in two lines of code.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fasm-ga/dirlist",
    project_urls={
        "Bug Tracker": "https://github.com/fasm-ga/dirlist/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)