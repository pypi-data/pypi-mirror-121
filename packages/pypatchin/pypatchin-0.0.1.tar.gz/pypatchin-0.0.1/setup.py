try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="pypatchin",
    description="Do you want a fast and clean solution to patch your files and repositories? Use Python pypatchin package!",
    license="GNU GENERAL PUBLIC LICENSE v3",
    version="0.0.1",
    author="Giulia Milan",
    author_email="giuliapuntoit96@gmail.com",
    maintainer="Giulia Milan",
    maintainer_email="giuliapuntoit96@gmail.com",
    url="https://github.com/giuliapuntoit/pypatch",
    download_url='https://github.com/giuliapuntoit/pypatch.git',
    keywords=['python', 'patch'],
    packages=['pypatchin'],
    install_requires=['diff_match_patch']
)
