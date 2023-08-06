import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="Suluoya",
    version="3.0.1",
    author="Suluoya",
    author_email="1931960436@qq.com",
    maintainer='Suluoya',
    maintainer_email='1931960436@qq.com',
    description="A package called Suluoya.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pandas',
                      'numpy',
                      'scipy',
                      'statsmodels',
                      'tqdm',  # 进度条
                      'baostock',  # 股票数据
                      'pretty_errors',  # 打印错误
                      'termcolor',  # 彩色打印
                      'matplotlib',
                      # 'lunar_python',  # 日期
                      # 'pysimplegui',  # gui
                      #'tushare',  # 股票数据

                      ]
)
