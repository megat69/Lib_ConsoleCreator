import setuptools

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "README.md not found."

setuptools.setup(
    name="console_file_explorer-megat69", # Replace with your own username
    version="0.0.1",
    author="megat69",
    description="Makes creating a console a simple task !",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/megat69/Lib_ConsoleCreator",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPL v3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)