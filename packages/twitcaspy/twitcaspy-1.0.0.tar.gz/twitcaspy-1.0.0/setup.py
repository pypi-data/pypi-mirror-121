import re
from setuptools import find_packages, setup

with open("README.md") as file:
    long_description = file.read()

tests_require = [
    "nose>=1.3.7,<2",
    "vcrpy>=4.1.1,<5",
    "python-dotenv>=0.17.1,<1",
]

examples_require = [
    "flask>=2.0.1,<3"
]

setup(
    long_description=long_description,
    project_urls={
        "Documentation": "https://twitcaspy.alma-field.com/",
        "Issue Tracker": "https://github.com/Alma-field/twitcaspy/issues",
        "Source Code": "https://github.com/Alma-field/twitcaspy",
    },
    download_url="",
    packages=find_packages(exclude=["tests", "examples"]),
    install_requires=[
        "requests>=2.25.1,<3",
        "requests_oauthlib>=1.3.0,<2",
    ],
    tests_require=tests_require,
    extras_require={
        "test": tests_require,
        "example": examples_require,
    },
    test_suite="nose.collector",
    keywords="twitcasting library",
    python_requires=">=3.7"
)
