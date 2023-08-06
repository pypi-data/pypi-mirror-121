import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

Project_Name="ON_Package"
User_Name="anishyadav-2021"

setuptools.setup(
    name=f"{Project_Name}-{User_Name}",
    version="0.0.1",
    author=User_Name,
    author_email="anishyadav1994@gmail.com",
    description="It is a Simple Neuron Implimentation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{User_Name}/{Project_Name}",
    project_urls={
        "Bug Tracker": f"https://github.com/{User_Name}/{Project_Name}/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "tqdm"
        "logging"
    ]
)