import setuptools

# https://towardsdatascience.com/how-to-publish-a-python-package-to-pypi-7be9dd5d6dcd
# https://mypy.readthedocs.io/en/stable/running_mypy.html#missing-type-hints-for-third-party-library
# https://github.dev/nawah-io/nawah_framework/tree/8f5930b607d7f2ea618a4dd05af548ab81bf443a
# python setup.py sdist bdist_wheel
# python -m twine upload -r testpypi --skip-existing dist/*
# python -m twine upload --skip-existing dist/*

# python setup.py sdist
# twine upload dist/*

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open("requirements.txt", "r") as fh:
#     requirements = fh.read().splitlines()

print(setuptools.find_packages())
# print(requirements)

setuptools.setup(
    name="site_scrapers",  # This is the name of the package
    version="0.0.22",  # The initial release version
    author="Dmitrijs Balcers",  # Full name of the author
    description="Scrape cars from dealerships",
    long_description=long_description,  # Long description read from the the readme file
    long_description_content_type="text/markdown",
    package_data={
        "models": ["py.typed"],
        "scrapers": ["py.typed"],
    },
    packages=setuptools.find_packages(),  # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  # Information to filter the project on PyPi website
    url="https://github.com/dmitrijs-balcers/site-scrapers/",
    python_requires='>=3.10',  # Minimum version requirement of the package
    py_modules=["site_scrapers"],  # Name of the python package
    install_requires=[
        "asyncio",
        "httpx",
        "returns",
        "gazpacho",
        "requests",
    ],  # Install other dependencies if any
    zip_safe=False,
)
