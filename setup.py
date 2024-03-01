import os

from setuptools import find_packages, setup


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()


version = "3.1.4"

tests_require = [
    "pytest==7.1.2",
    "pytest-cov",
]

dev_require = [
    "black==23.12.1",
    "flake8==4.0.1",
    "mypy==0.961",
] + tests_require

setup(
    name="graphql-ws",
    packages=find_packages(exclude=["tests"]),
    version=version,
    license="MIT",
    description="Websocket Backend for GraphQL Subscriptions",
    long_description=(read("README.md")),
    long_description_content_type="text/markdown",
    author="Syrus Akbary",
    author_email="me@syrusakbary.com",
    url="https://github.com/graphql-python/graphql-ws",
    download_url=f"https://github.com/graphql-python/graphql-ws/archive/{version}.tar.gz",
    keywords=["graphene", "graphql", "gql", "subscription"],
    install_requires=["graphene>=3.1", "graphql-core>=3.1"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    extras_require={
        "test": tests_require,
        "dev": dev_require,
    },
)
