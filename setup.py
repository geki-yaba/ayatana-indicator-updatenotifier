import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ayatana-indicator-updatenotifier",
    version="0.1.0",
    author="Hanno Zysik",
    author_email="none",
    description="A simple system packages update checker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AyatanaIndicators/ayatana-indicator-updatenotifier",
    packages=setuptools.find_packages(),
    python_requires='>=3',
    classifiers=
    [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    data_files=
    [
        ('bin',
        [
            'bin/ayatana-indicator-updatenotifier',
        ]),
        ('lib/ayatana-indicator-updatenotifier',
        [
            'libexec/ayatana-indicator-update-apt-get',
            'libexec/ayatana-indicator-updatecheck',
            'libexec/ayatana-indicator-updatelist',
            'data/updates.svg',
        ]),
        ('share/applications',
        [
            'data/ayatana-indicator-updatenotifier.desktop',
        ]),
    ],
)

# vim:expandtab
