import setuptools

with open("README.md", "r") as fo:
    long_description = fo.read()

setuptools.setup(
    name="morphe",
    version="0.2.0",
    author="B. T. Milnes",
    description="A Morphe implementation in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BenjaminTMilnes/MorphePython",
    packages=["morphe"]
)
