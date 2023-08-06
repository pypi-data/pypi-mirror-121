import pathlib2
from setuptools import setup

HERE = pathlib2.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(name='otp_generator',
      version='0.1.0',
      description='A Python tool to generate and verify One Time Password (OTP)',
      url='https://gitlab.com/frier17/otp_generator.git',
      author='https://gitlab.com/frier17/',
      author_email='frier17@a17s.co.uk',
      long_description=README,
      long_description_content_type="text/markdown",
      license="MIT",
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Security :: Cryptography',

          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.8",
      ],
      packages=['otp_generator', ],
      include_package_data=True
      )
