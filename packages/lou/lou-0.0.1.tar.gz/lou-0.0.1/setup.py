from setuptools import setup, find_packages


with open("README", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name="lou",
    version="0.0.1",
    python_requires=">=3.6",
    license="MIT",
    author="Bülent Aldemir",
    author_email="buelent@e-evolution.de",
    description="Lou",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    zip_safe=False,
)
