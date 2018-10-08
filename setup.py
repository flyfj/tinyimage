from setuptools import setup, find_packages, find_namespace_packages

# only used for dev.
requirements = []
test_requirements = []
try:
  from pipenv.project import Project
  from pipenv.utils import convert_deps_to_pip
  pfile = Project(chdir=False).parsed_pipfile
  requirements = convert_deps_to_pip(pfile['packages'], r=False)
  print(requirements)
  test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)
  print(test_requirements)
except:
  pass

setup(
    name="tinyimage",
    version="0.0.1",
    description="a lightweight image object library",
    keywords="computer vision image",
    url="https://github.com/VisualDataIO/tinyimage",
    author="Jie Feng",
    author_email="jiefeng@perceptance.io",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=requirements,
    tests_require=test_requirements,
    include_package_data=True,
    zip_safe=False)
