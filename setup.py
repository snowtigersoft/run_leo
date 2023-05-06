from setuptools import setup, find_packages

setup(
    name="run-leo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # 添加需要的依赖库
    ],
    python_requires=">=3.7",
    author="SnowTigerSoft",
    author_email="zhaochunyou@gmail.com",
    description="A Python package to run Leo function from python",
    url="https://github.com/snowtigersoft/run_leo",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
