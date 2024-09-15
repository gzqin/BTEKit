from setuptools import setup, find_packages

setup(
    name="BTEKit",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,  # 启用文件的自动包含
    package_data={
        # 包含 'scripts' 目录下的所有 .sh 和其他文件
        'BTEKit': ['scripts/*.sh', 'scripts/*.py', 'scripts/*'],  
    },
    entry_points={
        "console_scripts": [
            "btekit=BTEKit.main:main",  # BTEKit是命令名，BTEKit.main是Python模块，main是函数名
        ],
    },
    install_requires=[
        # 这里你可以列出任何必要的依赖项
    ],
    zip_safe=False,
    description="A toolkit for running scripts with easy selection interface",
    author="Guangzhao Qin, Yi Wei",
    author_email="qin.phys@gmail.com",
    url="https://example.com",
)
