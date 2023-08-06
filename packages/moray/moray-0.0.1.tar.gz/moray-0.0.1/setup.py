import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'moray',
    version = '0.0.1',
    author = 'hirorich',
    description = 'Package for creating HTML GUI using Python modules and JavaScript.',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/hirorich/moray',
    project_urls={
        'Bug Tracker': 'https://github.com/hirorich/moray/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows :: Windows 10',
    ],
    package_dir={'moray': 'moray'},
    packages = setuptools.find_packages(include=['moray', 'moray.*']),
    package_data={
        'moray': [
            '_module/py/template/*.js',
            '_module/static/*.js',
        ],
    },
    python_requires = '>=3.9',
    keywords = ['gui', 'html', 'javascript'],
    install_requires = ['bottle-websocket', 'requests', 'Jinja2'],
)
