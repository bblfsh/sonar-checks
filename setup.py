import glob
import sys
from setuptools import setup, find_packages

description = long_descr = "Library implementing Sonar Source checks using the babelfish project"

VERSION = "0.4.0"

setup(
        name = "bblfsh_sonar_checks",
        version = VERSION,
        description = description,
        license="Apache 2.0",
        author="source{d}",
        author_email="language-analysis@sourced.tech",
        url="https://github.com/bblfsh/sonar_source_checks",
        download_url="https://github.com/bblfsh/sonar_source_checks",
        packages=find_packages(),
        keywords=["babelfish", "uast", "static analysis", "java"],
        install_requires=["bblfsh>=2.11.2"],
        package_data={"": ["LICENSE", "README.md", "MAINTAINERS"] +
                          glob.glob("bblfsh_sonar_checks/fixtures/*/*")},
        include_package_data = True,
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: Apache Software License",
            "Operating System :: POSIX",
            "Programming Language :: Python :: 3.4",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Topic :: Software Development :: Libraries"
        ],
        entry_points={
            "console_scripts": [
                "sonarbblfsh = bblfsh_sonar_checks.__main__:main"
            ]
        },
)
