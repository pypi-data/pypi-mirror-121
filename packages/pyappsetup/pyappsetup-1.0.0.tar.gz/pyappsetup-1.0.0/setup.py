import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyappsetup", # Replace with your own username
    version="1.0.0",
    author="Louis DEVIE",
    author_email="louisdevie.contact@gmail.com",
    description="Reading / writing configuration files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/louisdevie/pyappsetup",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.8",
)