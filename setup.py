import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ayatana-indicator-updatenotifier",
    version="0.0.1",
    author="Hanno Meyer-Thurow",
    author_email="none",
    description="A simple system packages update checker",
    long_description=long_description,
    long_description_content_type="text/plain",
    url="https://github.com/AyatanaIndicators/ayatana-indicator-updatenotifier",
    packages=setuptools.find_packages(),
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# vim:expandtab
