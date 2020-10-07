from setuptools import setup, find_packages

setup(
    name = 'sendgrowl',
    version = '0.3.2',
    author = 'Hadi Cahyadi LD',
    author_email = 'cumulus13@gmail.com',
    description = ('simple send notification to growl based on gntplib'),
    license = 'MIT',
    keywords = "growl terminal gntplib gntp",
    url = 'https://github.com/cumulus13/sendgrowl',
    scripts = [],
    py_modules = ['sendgrowl'],
    packages = find_packages(),
    install_requires = [],
    download_url = 'https://github.com/cumulus13/sendgrowl/tarball/master',
    install_requires=[
        'gntplib',
        'configset',
        'configparser'
    ],
    # TODO
    #entry_points={
    #    "console_scripts": ["drawille=drawille:__main__"]
    #},
    entry_points = {
         "console_scripts": ["sendgrowl = sendgrowl:usage",]
    },
    classifiers = [
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        'Environment :: Console',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
