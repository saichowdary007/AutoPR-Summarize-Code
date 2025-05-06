from setuptools import setup, find_packages

setup(
    name="pr-assistant",
    version="0.1.0",
    packages=find_packages(),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "fastapi",
        "uvicorn",
        "pydantic",
        "python-dotenv",
        "httpx",
        "PyGithub",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "pylint",
        ],
    },
) 