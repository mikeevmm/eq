import setuptools
from eq.version import __version__

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

with open('requirements.txt', 'r') as requirements:
    install_requires = [
        line[:line.find('==')]
        for line in requirements.readlines()]

setuptools.setup(
    name='eq',
    version=__version__,
    author='Miguel Murça',
    author_email='miguelmurca+eq@gmail.com',
    description='Render LaTeX equations into the clipboard.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mikeevmm/eq',
    project_urls = {
        'Bug Tracker': 'https://github.com/mikeevmm/eq/issues'
    },
    license='GPLv2',
    packages=['eq'],
    entry_points = {
        'console_scripts': [
            'eq=eq.eq:main'
        ]
    },
    install_requires=install_requires,
)
