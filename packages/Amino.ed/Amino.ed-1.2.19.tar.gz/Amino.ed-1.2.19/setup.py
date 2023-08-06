from setuptools import setup, find_packages

with open("README.md", "r") as stream:
    long_description = stream.read()

setup(
    name = 'Amino.ed',
    version = '1.2.19',
    url = 'https://github.com/Alert-Aigul/Amino.ed',
    download_url = 'https://github.com/Alert-Aigul/Amino.ed/tarball/master',
    license = 'MIT',
    author = 'Alert',
    author_email = 'alertaigul@gmail.com',
    description = 'A library to create Amino bots.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    keywords = [
        'aminoapps',
        'amino-py',
        'amino',
        'amino-bot',
        'narvii',
        'api',
        'python',
        'python3',
        'python3.x',
        'slimakoi',
        'unofficial',
        "alert",
        "fix"
    ],
    install_requires = [
        'setuptools',
        'requests',
        'six',
        'websocket-client==0.57.0',
        'json_minify'
    ],
    setup_requires = [
        'wheel'
    ],
    packages = find_packages()
)
