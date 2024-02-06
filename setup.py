# coding=utf-8

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name = "cuteFC",
    version = "1.0.0",
    description = "Regenotyping structural variants through an accurate and efficient force-calling method",
    author = "Jiang Tao & Cao Shuqi",
    author_email = "tjiang@hit.edu.cn",
    url = "https://github.com/tjiangHIT/cuteFC",
    license = "MIT",
    packages = find_packages("src"),
    package_dir = {"": "src"},
    data_files = [("", ["LICENSE"])],
    scripts=['src/cuteFC/cuteFC'],
    # long_description = LONG_DESCRIPTION,
    long_description = readme,
    long_description_content_type = 'text/markdown',
    zip_safe = False,
    install_requires = ['scipy', 'pysam', 'Biopython', 'Cigar', 'numpy', 'pyvcf3', 'scikit-learn']
)
