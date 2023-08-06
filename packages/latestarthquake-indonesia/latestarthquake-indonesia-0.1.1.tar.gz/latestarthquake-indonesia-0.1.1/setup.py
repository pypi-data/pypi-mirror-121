"""
https://packaging.python.org/tutorials/packaging-projects/
Markdown guides: https://www.markdownguide.org/cheat-sheet/
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="latestarthquake-indonesia",
    version="0.1.1",
    author="mizan toyyibun",
    author_email="untirta.mizan62@gmail.com",
    description="This package will give us information about the latest earthquake in Indonesia. The data taken from "
                "BMKG (Meteorology, Climatology, and Geophysics Agency).",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wearenotrobot/latest-indonesian-earthquake",
    project_urls={
        "Github": "https://github.com/wearenotrobot/latest-indonesian-earthquake",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where="src"),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
