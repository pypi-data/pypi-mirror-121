import setuptools
with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BIT_framework",
    version="0.0.0",
    author="wxl",
    author_email="847084723@qq.com",
    description="A dialog framework",
    packages=setuptools.find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ]
)