from setuptools import setup, find_packages

with open("README.md", "r", encoding = "UTF-8") as file:
    long_desc = file.read()
 
setup(
    name = "aerforge",
    version = "0.0.1",
    description = "A game engine made with SDL.",
    long_description = long_desc,
    long_description_content_type = "text/markdown",
    url = "https://github.com/Aermoss/AerForge",
    author = "Yusuf Rencber",
    author_email = "yusufrencber546@gmail.com",
    license = "MIT",
    keywords = "game engine",
    packages = find_packages(),
    install_requires = [""]
)