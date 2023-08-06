import setuptools
setuptools.setup(
    name="infra2conn",
    version="0.0.3",
    author="Renzo Becerra",
    description="Infra 2.0 Connections",
    packages=["infra2conn"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=["simple-salesforce==1.11.3", "requests==2.24.0", "pyspark==3.1.2", "pandas==1.1.3"],
    python_requires='>=3.6',
    entry_points={"console_scripts": ["infra2conn=infra2conn.cli:main"]}
)

