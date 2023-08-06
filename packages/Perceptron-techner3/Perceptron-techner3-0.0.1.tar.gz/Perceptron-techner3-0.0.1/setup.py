import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

PROJECT_NAME ="Perceptron"
USERNAME ="techner3"
setuptools.setup(
    name=f"{PROJECT_NAME}-{USERNAME}",
    version="0.0.1",
    author=USERNAME,
    author_email="k.balamurali303@gmail.com",
    description="Its an implementation of a neuron",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/techner3/Perceptron",
    project_urls={
        "Bug Tracker": "https://github.com/techner3/Perceptron/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    install_requires=["numpy","tqdm"]
)