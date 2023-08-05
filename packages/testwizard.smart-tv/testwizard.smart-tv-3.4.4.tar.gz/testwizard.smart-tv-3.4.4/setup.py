import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testwizard.smart-tv",
    version="3.4.4",
    author="Eurofins Digital Testing - Belgium",
    author_email="testwizard-support@eurofins-digitaltesting.com",
    description="Testwizard for Smart TV testobjects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.eurofins-digitaltesting.com/testwizard/",
    packages=['testwizard.smart_tv'],
    install_requires=[
        'testwizard.test==3.4.4',
        'testwizard.testobjects-core==3.4.4',
        'testwizard.commands-audio==3.4.4',
        'testwizard.commands-mobile==3.4.4',
        'testwizard.commands-powerswitch==3.4.4',
        'testwizard.commands-remotecontrol==3.4.4',
        'testwizard.commands-video==3.4.4',
        'testwizard.commands-camera==3.4.4'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
)













