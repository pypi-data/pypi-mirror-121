from setuptools import Extension, setup, find_packages
from Cython.Build import cythonize

with open("README.md", "r") as fh:
    long_description = fh.read()

ext_modules = [
    Extension(
        "sparsedist._nearest_neighbours",
        ["sparsedist/_nearest_neighbours.pyx"],
        language="c++",
        extra_compile_args=["-Wno-unused-function", "-Wno-maybe-uninitialized", "-O3", "-ffast-math", '-fopenmp', '-std=c++11'],
        extra_link_args=['-fopenmp', '-std=c++11'],
    )
]

setup(
    name='sparsedist',
    version="0.0.3",
    author="pbcquoc",
    author_email="pbcquoc@gmail.com",
    description="faster parallel pairwise sparse distance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pbcquoc/sparsedist",
    install_requires=["numpy", "scipy>=0.16", "tqdm>=4.27"],
    setup_requires=["Cython>=0.24", "scipy>=0.16"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    package_data={"sparsedist": ["nearest_neighbours.h", '_nearest_neighbours.pyx']},
    python_requires='>=3.6',
    ext_modules=cythonize(ext_modules, language_level = "3"),
)
