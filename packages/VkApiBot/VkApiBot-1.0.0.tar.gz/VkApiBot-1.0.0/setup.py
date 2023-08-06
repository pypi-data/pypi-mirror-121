import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

requirements = ["vk_api", "retry"]

setuptools.setup(
    name="VkApiBot",
    version='1.0.0',
    author="Sicquze",
    author_email="Sicquzeeee@gmail.com",
    description="Very well python library for easy work with vk_api lib.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8",
)