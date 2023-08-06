from setuptools import find_packages, setup

# with open("VERSION") as version_file:
#     version = version_file.read().strip()

setup(
    name="paul2gans",
    version='0.1.5',
    description="Backend package to generate AI Posters.",
    author="paulilhe",
    author_email="paul.ilhe@gmail.com",
    url="https://github.com/paulilhe/gans",
    license="Proprietary",
    packages=find_packages("src", exclude=["*.tests"]),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.7",
    install_requires=[
        "attrs",
        "tensorflow~=2.3",
        "tensorflow-addons~=0.13",
        "pip-tools~=5.5",
        "matplotlib",
        "click"
    ],
    entry_points={"console_scripts": ["gans=paul2gans.pipelines:cli", "wgan=paul2gans.pipelines.wgan:wgan"]},
)
