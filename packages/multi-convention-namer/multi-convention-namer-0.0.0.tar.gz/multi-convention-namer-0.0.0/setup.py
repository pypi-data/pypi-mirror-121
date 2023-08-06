import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "multi-convention-namer",
    "version": "0.0.0",
    "description": "A string manipulation library to facilitate dealing with multiple naming conventions",
    "license": "Apache-2.0",
    "url": "https://github.com/myhelix/multi-convention-namer",
    "long_description_content_type": "text/markdown",
    "author": "Andrew Hammond<andrew.george.hammond@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/myhelix/multi-convention-namer"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "multi_convention_namer",
        "multi_convention_namer._jsii"
    ],
    "package_data": {
        "multi_convention_namer._jsii": [
            "multi-convention-namer@0.0.0.jsii.tgz"
        ],
        "multi_convention_namer": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii>=1.34.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
