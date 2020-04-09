from setuptools import setup

setup(
    name='captchaMiddleware',
    version='1.0.0',
    description='Check for a CAPTCHA test and try solving it',
    long_description=open('README.rst').read(),
    keywords='scrapy web-scraping captcha amazon ocr',
    license='New BSD License',
    author="Owen Miller",
    author_email='owen9825@gmail.com',
    url='kokociel.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Scrapy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Framework :: Scrapy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=[
        'captchaMiddleware',
    ],
    install_requires=[
        'pytesseract',
        'numpy',
        'scipy',
        'scrapy',
        'bs4',
        'opencv-python',
        'imutils'
    ],
    test_suite='nose.collector',
    tests_require=['nose']
)
