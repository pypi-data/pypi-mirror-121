import setuptools


name = 'cqh_image'
long_description = """cqh image
========================================

only work on windows

作用是吧windows粘贴板里面的图片转成base64,然后再写道粘贴板里面

因为vscode remote暂时不支持readImage




"""



version = "0.0.4"

setuptools.setup(
    name=name,  # Replace with your own username
    version=version,
    author="chenqinghe",
    author_email="1832866299@qq.com",
    description="cqh utils function",
    long_description=long_description,
    long_description_content_type='',
    url="https://github.com/chen19901225/cqh_util",
    packages=setuptools.find_packages(),
    install_requires=[
        "click",
        "pywin32",
        "pillow",
        "tornado",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    entry_points={
        "console_scripts": [
            "cqh_image=cqh_image.run:cli",
        ],
    },
    python_requires='>=3.6',
    include_package_data=True
)