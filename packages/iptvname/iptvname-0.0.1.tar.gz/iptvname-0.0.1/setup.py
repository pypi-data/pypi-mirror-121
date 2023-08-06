import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="iptvname",
    version="0.0.1",
    license='MIT',
    author="Sang Woo",
    author_email="sanguh096@gmail.com",
    description="Collection of publicly available IPTV channels name from all over the world",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sktkddn777/iptv",
    packages=setuptools.find_packages(),
    classifiers=[
        # 패키지에 대한 태그
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],

    python_requires='>=3.6',
)