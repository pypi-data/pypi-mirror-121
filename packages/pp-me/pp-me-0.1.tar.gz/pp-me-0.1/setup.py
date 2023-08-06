from setuptools import setup

from pp_me import version

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pp-me",
    packages=["pp_me"],
    version=version.version(),
    description="Pretty Print Me!",
    author="Nicholas M. Synovic",
    author_email="nicholas.synovic@gmail.com",
    license="BSD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://nicholassynovic.github.io",
    project_urls={
        "Bug Tracker": "https://github.com/NicholasSynovic/pp-me/issues",
        "GitHub Repository": "https://github.com/NicholasSynovic/pp-me",
    },
    keywords=["pretty", "terminal", "json"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
    python_requires=">=3.9",
    install_requires=[],
    entry_points={
        "console_scripts": [
            "pp-me = pp_me.main:main",
        ]
    },
)
