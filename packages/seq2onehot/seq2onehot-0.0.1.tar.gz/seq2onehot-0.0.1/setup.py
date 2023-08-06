import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    description="encoding a biological sequence to a one-hot numpy array",
    install_requires=["numpy"],
    name="seq2onehot",
    version="0.0.1",
    entry_points={
        'console_scripts': [
            'seq2onehot=seq2onehot.main:main',
        ],
    },
    author="Akihiro Kuno",
    author_email="akuno@md.tsukuba.ac.jp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akikuno/seq2onehot",
    packages=setuptools.find_packages(
        where='src',
    ),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
