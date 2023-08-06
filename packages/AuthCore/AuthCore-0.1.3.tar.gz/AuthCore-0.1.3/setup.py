import setuptools

with open("./AuthCore/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='AuthCore',
    version='0.1.3',
    description='AuthCore',
    author='Theta',
    license='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(exclude=["pymongo", "numpy"]),
    package_data={
        "": ["*.txt", "*.py", "*.md"]
    },
    zip_safe=False
)
