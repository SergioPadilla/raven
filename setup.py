from pathlib import Path

from setuptools import setup, find_packages


setup(
    name='RAVEN',
    version=Path('VERSION.txt').read_text().strip(),
    description='',
    long_description='',
    license='MIT',
    url='https://github.com/SergioPadilla/raven',
    download_url='https://github.com/SergioPadilla/raven',
    author='Sergio Padilla López',
    author_email='splsergiopadilla@gmail.com',

    packages=find_packages('src'),
    package_dir={'': 'src'},

    python_requires='>=3.6',
    install_requires=Path('requirements.txt').read_text().splitlines(),

    entry_points={'console_scripts': ['raven=raven:main']},
)
