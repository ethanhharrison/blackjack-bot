from setuptools import setup, find_packages

setup(
    name="blackjack-bot",
    version="0.1.0",
    description="A custom Blackjack environment for OpenAI Gym.",
    author="E Harrison",
    author_email="ehharrison@berkeley.edu",
    url="https://github.com/ethanhharrison/blackjack-bot",
    packages=find_packages(),
    install_requires=[
        "gym>=0.21",
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)