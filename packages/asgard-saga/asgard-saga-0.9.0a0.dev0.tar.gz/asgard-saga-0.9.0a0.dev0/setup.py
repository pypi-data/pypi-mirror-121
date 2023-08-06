from setuptools import setup, find_packages

with open("README.md", mode="r", encoding="utf-8") as readme:
    long_description = readme.read()

with open("requirements.txt", mode="r", encoding="utf-8") as requirements:
    requirements = requirements.read()


setup(
    name='asgard-saga',
    version='0.9.0A.dev0',
    author='Alex Sáenz Rojas',
    author_email='cnca@cenat.ac.cr',
    license='GNU General Public License v3.0',
    description='A tool for genomic sequential analysis automation.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/CNCA_CeNAT/asgard',
    package_dir={'asgard': 'src'},
    packages=find_packages(),
    install_requires=[requirements],
    python_requires='>=3.7',
    classifiers=["Intended Audience :: Science/Research",
                 "Framework :: Sphinx",
                 "Development Status :: 3 - Alpha",
                 "Environment :: Console",
                 "Programming Language :: Python :: 3.7",
                 "Operating System :: POSIX :: Linux",
                 "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                 "Topic :: Scientific/Engineering :: Bio-Informatics"
                 ],
    entry_points='''
        [console_scripts]
        asgard=src.main:main
    '''
)
