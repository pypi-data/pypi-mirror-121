import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mptools",
    version="1.0.8",
    author="Manuele Pesenti",
    author_email="manuele@inventati.org",
    description="A very custom collection of development shared libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manuelep/mptools",
    project_urls={
        "Bug Tracker": "https://github.com/manuelep/mptools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "py4web",
        "pytz>=2020.1",
        "pandas>=1.0.3",
        "matplotlib",
        "numpy",
        "diskcache",
        "pytopojson"
    ]
)
