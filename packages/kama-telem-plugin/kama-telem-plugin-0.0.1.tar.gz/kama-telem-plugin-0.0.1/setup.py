import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
  name="kama-telem-plugin",
  version="0.0.1",
  author="NMachine",
  author_email="xavier@nmachine.io",
  description="Telemetry plugin for the kama-sdk-py",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/nmachine-io/kama-sdk-py",
  package_data={
    'kama_telem_plugin': [
      'assets/*.*',
      'descriptors/**'
    ]
  },
  include_package_data=True,
  install_requires=[
    'kama-sdk-py',
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  python_requires='>=3.8'
)
