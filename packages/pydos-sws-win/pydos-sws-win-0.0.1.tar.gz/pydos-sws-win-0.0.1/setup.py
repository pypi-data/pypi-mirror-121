import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydos-sws-win",
    version="0.0.1",
    author="PT Studio",
    author_email="jjy1207826398@163.com",
    description="py-dos's softwares.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/yizhigezi_yijiafeiji/pydos",
    project_urls={
        "Bug Tracker": "https://gitee.com/yizhigezi_yijiafeiji/pydos/issues",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Win32 (MS Windows)",
        "Programming Language :: Python :: 3.8"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)