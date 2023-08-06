import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dietkit",
    version="0.0.11",
    author="Soohyeok Kim",
    author_email="sooo@unist.ac.kr",
    description="Tools for management diet and its components",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pki663/dietkit",
    project_urls={
        "Bug Tracker": "https://github.com/pki663/dietkit/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Natural Language :: Korean",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
    ],
    package_dir={"": "src"},
    package_data={"": ["*.csv"]},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    include_package_data=True
)