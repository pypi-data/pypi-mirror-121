import setuptools  # 模块

# 让readme文件以只读的形式
with open("README.md", "rb") as f:
    description = f.read().decode("utf-8")

setuptools.setup(
    name="19434010112",              # 当包名已经出现在pypi中已经被别人发布过，你再发布就会报403错误
    version="1.0",
    packages=setuptools.find_packages(),
    aythor="laohu",
    author_email="aaa@163.com",
    description="一个打包案例",
    long_description=description,
    python_requires=">=3.7" # python的最低版本
)