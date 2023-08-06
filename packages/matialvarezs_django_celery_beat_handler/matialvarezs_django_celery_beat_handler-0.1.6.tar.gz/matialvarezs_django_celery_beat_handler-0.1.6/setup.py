from distutils.core import setup
import setuptools

setup(
    name='matialvarezs_django_celery_beat_handler',
    packages=['matialvarezs_django_celery_beat_handler'],  # this must be the same as the name above
    version='0.1.6',
    install_requires=[
        'django-ohm2-handlers-light',
        'django-celery-beat'
    ],
    include_package_data=True,
    description='Easy handler django celery beat models: create, filter, get_or_none, get_or_create, update operations',
    author='Matias Alvarez Sabate',
    author_email='matialvarezs@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3.5',
    ],
)