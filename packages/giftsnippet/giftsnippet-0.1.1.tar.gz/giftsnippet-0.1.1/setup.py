import pathlib
import pkg_resources
import setuptools

with pathlib.Path('./requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

def readme():
    with open('README.md') as f:
        return f.read()

setuptools.setup(name='giftsnippet',
      version='0.1.1',
      description='Integrate highlighted source code images with data uris into your gift questions',
      long_description=readme(),
      long_description_content_type='text/markdown',
      keywords='gift moodle code-formatting',
      url='http://github.com/stefanhuber/giftsnippet',
      author='Stefan Huber',
      author_email='mail@stefanhuber.at',
      license='BSD',
      packages=['giftsnippet'],
      install_requires=install_requires,
      test_suite="giftsnippet.tests",
      include_package_data=True,
      zip_safe=False,
     entry_points={
         'console_scripts': ['giftsnippet=giftsnippet.console:main'],
     })
