nlp-text-corrector
==================

``nlp-text-corrector`` is a python package that helps post process the raw ASR output

- Parsing of numbers expressed as words in English and convert them to integer values.
- Detection of ordinal, cardinal and decimal numbers in a stream of Englishwords and get their decimal digit representations. 
- Detection of email/website addresses as words in English and convert them to proper email/website format.
- Detection of times expressed as raw text in English to proper time format.

Compatibility
-------------

Tested on python 3.7. Requires Python >= 3.6.

License
-------

This sofware is distributed under the MIT license of which you should have received a copy (see LICENSE file in this repository).

Installation
------------

``nlp-text-corrector`` does not depend on any other third party package.

To install nlp-text-corrector in your (virtual) environment::

    pip install nlp-text-corrector

That's all folks!

Usage examples
--------------

Parse and convert
~~~~~~~~~~~~~~~~~


Examples:

.. code-block:: python

    >>> from nlp_text_corrector import asr_post_process

    >>> asr_post_process.convert("Book twenty first century marvel movie for my two kids of age nine and thirteen at eight twenty two pm tonight")
    Book 21st century marvel movie for my 2 kids of age 9 and 13 at 8:22 pm tonight

    >>> asr_post_process.convert("fifty-one million five hundred seventy-eight thousand three hundred two")
    51578302

    >>> asr_post_process.convert("eighty-one")
    81

    >>> asr_post_process.convert("On May twenty-third , I bought twenty-five cows, twelve chickens and one hundred twenty five point four zero kg of potatoes.")
    On May 23rd, I bought 25 cows, 12 chickens and 125.40 kg of potatoes.

Contribute
----------

Join us on https://github.com/iAmPlus/nlp-text-corrector
