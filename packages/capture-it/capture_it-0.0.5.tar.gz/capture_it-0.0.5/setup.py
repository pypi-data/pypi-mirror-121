import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="capture_it",
    version="0.0.5",
    author="ALIASGAR - ALI",
    author_email="aholo2000@gmail.com",
    description="Excel Facts File Generate from Networking Device Output|Config",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aliasgar1978/capture_it",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires= ['nettoolkit', 'paramiko', 'netmiko']
)

