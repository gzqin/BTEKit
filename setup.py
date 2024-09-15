from setuptools import setup, find_packages

setup(
    name="BTEKit",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,  
    package_data={
        'BTEKit': ['scripts/*.sh', 'scripts/*.py', 'scripts/*'],  
    },
    entry_points={
        "console_scripts": [
            "btekit=BTEKit.main:main", 
        ],
    },
    install_requires=[
    ],
    zip_safe=False,
    description="A toolkit for running scripts with easy selection interface",
    author="Guangzhao Qin, Yi Wei",
    author_email="qin.phys@gmail.com",
    url="https://github.com/gzqin/BTEkit",
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: POSIX :: Linux",  # This specifies Linux
],
python_requires='>=3.6',
)
