from setuptools import setup
import os


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('simple_NER')

setup(
    name='simple_NER',
    version='0.4.1',
    packages=['simple_NER', 'simple_NER.rules', 'simple_NER.annotators',
              'simple_NER.annotators.remote', 'simple_NER.annotators.utils',
              'simple_NER.annotators.utils.keywords'],
    url='https://github.com/OpenJarbas/simple_NER',
    package_data={'': extra_files},
    include_package_data=True,
    license='MIT',
    author='jarbasAI',
    install_requires=["padaos", "fann2==1.0.7", "padatious", "nltk",
                      "quantulum3", "requests", "lingua_franca>=0.1.0",
                      "pyspotlight"],
    author_email='jarbasai@mailfence.com',
    description='rule based NER'
)
