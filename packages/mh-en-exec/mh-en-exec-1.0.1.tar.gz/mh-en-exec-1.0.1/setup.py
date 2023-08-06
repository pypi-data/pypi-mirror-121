from setuptools import setup, find_packages

with open("README.md", "r") as fh:
  long_description = fh.read()

setup(
  name='mh-en-exec',
  version='1.0.1',
  description='Package for executing machine heads external nodes',
  long_description=long_description,
  long_description_content_type="text/markdown",
  url='https://mheads.net/external_nodes',
  author='Opus',
  author_email='mh@opus.co.jp',
  license='MIT',
  package_dir={"": "src"},
  packages=['mh_en_exec', 'mh_en_exec.connection', 'mh_en_exec.nodes', 'mh_en_exec.nodes.views', 'mh_en_exec.resource'],
  zip_safe=False,
  keywords=['automation', 'test', 'machine heads', 'custom', 'node'],
  install_requires=[
      'grpcio>=1.37.0',
      'grpcio-tools>=1.37.0',
      'opencv-python>=4.1.2.30'
  ],
  classifiers=[
      'Development Status :: 5 - Production/Stable',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3.6',
      'Operating System :: OS Independent'
  ],
  python_requires=">=3.6"
)
