import setuptools

keywords = ['flask', 'directory structure', 'cookie cutter'
            'venv']

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'template_flask',
    version = "0.0.3",
    author = 'Zach Beebe',
    author_email = 'z.beebe@yahoo.com',
    description = 'Python module for creating a template flask app structure and virtual environment',
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = 'https://github.com/zacharybeebe/basic_flask_setup',
    license = 'MIT',
    packages = setuptools.find_packages(),
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"],
    keywords = keywords,
    python_requires = '>=3.6',
    py_modules = ['template_flask']
)
