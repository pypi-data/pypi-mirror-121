import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    description="decode a one-hot numpy array to biological sequences",
    install_requires=["numpy"],
    name="onehot2seq",
    version="0.0.2",
    entry_points={
        'console_scripts': [
            'onehot2seq=onehot2seq.main:main',
        ],
    },
    author="Akihiro Kuno",
    author_email="akuno@md.tsukuba.ac.jp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akikuno/onehot2seq",
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
