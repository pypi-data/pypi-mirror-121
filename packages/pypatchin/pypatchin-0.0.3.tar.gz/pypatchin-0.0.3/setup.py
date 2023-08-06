import pypandoc

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    long_description = pypandoc.convert('README.md', 'rst')
    long_description = long_description.replace("\r", "")  # Do not forget this line
except OSError:
    print("Pandoc not found. Long_description conversion failure.")
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding="utf-8") as f:
        long_description = f.read()

setup(
    name="pypatchin",
    description="Do you want a fast and clean solution to patch your files and repositories? Use Python pypatchin package!",
    long_description=long_description,
    license="GNU GENERAL PUBLIC LICENSE v3",
    version="0.0.3",
    author="Giulia Milan",
    author_email="giuliapuntoit96@gmail.com",
    maintainer="Giulia Milan",
    maintainer_email="giuliapuntoit96@gmail.com",
    url="https://github.com/giuliapuntoit/pypatch",
    download_url='https://github.com/giuliapuntoit/pypatch.git',
    keywords=['python', 'patch'],
    packages=['pypatchin'],
    install_requires=['diff_match_patch', 'pypandoc']
)
