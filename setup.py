import os
import setuptools

here = os.path.abspath(os.path.dirname(__file__))
DESCRIPTION = "A args parse package with '-', '--', ',' '|', '{', '}', '[', ']', '=' and character patterns."

try:
    with open(os.path.join(here, "README.md"), "r") as fh:
        long_description = fh.read()
except Exception as err:
    long_description = DESCRIPTION

setuptools.setup(
    name="akparse",
    version="0.1.8",
    author="AbsentM",
    author_email="absentm@163.com",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/absentm/akparse",
    project_urls={
        "Bug Tracker": "https://github.com/absentm/akparse/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    # packages=setuptools.find_packages(),
    python_requires=">=2.6",
)
