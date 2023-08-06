import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyhill",
    version="0.0.1",
    author="Yek",
    author_email="gwojtysiak34@gmail.com",
    description="Easily modify the readwritememory of Brick Hill.",
    long_description=long_description, # don't touch this, this is your README.md
    long_description_content_type="text/markdown",
    url="https://github.com/Yekc/PyHill/tree/main",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)