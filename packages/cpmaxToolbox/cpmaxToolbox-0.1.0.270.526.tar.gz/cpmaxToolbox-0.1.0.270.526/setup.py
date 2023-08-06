import pathlib
from setuptools import setup, find_packages
import datetime

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

now = datetime.datetime.now()
v_dt = now.strftime("%j")+"."+f"{60*now.hour+now.minute}"

VERSION = "0.1.0."+v_dt

classifiers = [
    "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Development Status :: 4 - Beta",
    "Topic :: Scientific/Engineering",
]

setup(
    name="cpmaxToolbox",
    version=VERSION,
    description="Toolbox for cp.max Rotortechnik GmbH & Co. KG",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/JRoseCPMax/cpmax_toolbox",
    author="Jonas Rose",
    author_email="j.rose@cpmax.com",
    license="GPLv3",
    python_requires='>=3.0',
    classifiers=classifiers,
    packages=find_packages(),
    include_package_data=True,
    install_requires=["pandas", "numpy", "rich"],
)