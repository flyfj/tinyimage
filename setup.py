from setuptools import setup, find_packages

with open("./configs/requirements.txt", "r") as f:
  dep_packages = f.readlines()
  # remove local install.
  dep_packages = [x.strip() for x in dep_packages if not x.startswith("-e")]

setup(
    name="deepimage",
    version="0.0.3",
    description="a lightweight image object library",
    keywords="computer vision image",
    url="https://flyfj@bitbucket.org/flyfj/deepimage.git",
    author="Jie Feng",
    author_email="jiefengdev@gmail.com",
    packages=find_packages("./"),
    install_requires=dep_packages,
    include_package_data=True,
    zip_safe=False)
