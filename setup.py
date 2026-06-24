from setuptools import setup, find_packages

setup(
    name="turkish-nlp-toolkit",
    version="0.1.0",
    author="Enis Dogan",
    author_email="enis-dogan@outlook.com",
    description="A comprehensive NLP toolkit for the Turkish language",
    long_description=open("README.md", encoding="utf-8").read() if __import__("os").path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/ensibey/turkish-nlp-toolkit",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Linguistic",
        "Natural Language :: Turkish",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "bert": ["torch>=1.9.0", "transformers>=4.20.0", "scikit-learn>=1.0.0"],
        "dev": ["pytest>=7.0.0"],
    },
    keywords=["turkish", "nlp", "bert", "tokenizer", "turkce", "doga-dil-isleme"],
)
