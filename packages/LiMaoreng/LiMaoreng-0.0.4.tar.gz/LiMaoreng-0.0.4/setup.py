import setuptools

setuptools.setup(
    name="LiMaoreng",  # 库的名字
    version="0.0.4",  # 库的版本号，后续更新的时候只需要改版本号就行了
    author="李茂仍",
    author_email="2324412934@qq.com",
    description="""李茂仍的常用Python小功能。
    0.0.1版为测试版，无具体功能。
    0.0.2版提供了李茂仍常用的简单脚本功能。
    0.0.3版修复了部分错误
    0.0.4版移除了“锁定”函数的递归，改为循环""",  # 介绍
    long_description_content_type="text/markdown",
    url="https://github.com/",
    packages=setuptools.find_packages(),
    install_requires=['pyautogui', "smtplib", "email", "pycaw"],  # 用户安装后，系统会自动安装第三方库
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License ",
        "Operating System :: OS Independent",
    ],
)
'''
python setup.py sdist
twine upload dist/*
LiMaoreng
密码'''
