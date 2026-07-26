import setuptools

with open("README.md", "r", encoding="utf-8") as fd:
    long_description = fd.read()

setuptools.setup(
    name="drone_swarm_gcs",
    version="1.0.0",
    packages=setuptools.find_packages(),
    description="Python package for drone swarm coordination and control",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ishver Chandra Jaiswal",
    author_email="ishverjaiswal40@gmail.com",
    url="https://github.com/ishverjaiswal/Drone_Swarm",
    install_requires=[
        "numpy",
        "opencv-python",
        "av",
        "pillow"
    ],
    python_requires=">=3.6",
)