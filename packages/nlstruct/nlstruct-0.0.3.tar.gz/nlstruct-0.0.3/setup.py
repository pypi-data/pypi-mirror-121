import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setuptools.setup(
        name="nlstruct",
        version="0.0.3",
        author="Perceval Wajsburt",
        author_email="perceval.wajsburt@sorbonne-universite.fr",
        license='BSD 3-Clause',
        description="Natural language structuring library",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/percevalw/nlstruct",
        packages=setuptools.find_packages(),
        package_data={'': ['example.env']},
        include_package_data=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=[
            "numpy~=1.19.5",
            "torch~=1.7.1",
            "unidecode~=1.1.2",
            "einops~=0.3.0",
            "transformers>=4.3.0<=4.11.2",
            "optuna~=2.5.0",
            "tqdm~=4.56.0",
            "sklearn~=0.0",
            "scikit-learn~=0.24.1",
            "pandas~=1.2.1",
            "pytorch_lightning>=1.1.7<=1.4.9",
            "rich_logger~=0.1.4",
            "sentencepiece~=0.1.95",
            "xxhash~=2.0.0",
            "regex~=2020.11.13",
            "parse~=1.19.0",
        ]
    )
