=========
pdfreader
=========
:Info: See `the tutorials & documentation <https://pdfreader.readthedocs.io>`_ for more information.
See `GitHub <https://github.com/maxpmaxp/pdfreader>`_ for the latest source.
:Author & Maintainer: Maksym Polshcha <maxp@sterch.net>


About
=====

*pdfreader* is a Pythonic API for:
    * extracting texts, images and other data from PDF documents
    * accessing different objects within PDF documents


*pdfreader* is **NOT** a tool:
    * to create or update PDF files
    * to split PDF files into pages or other pieces
    * convert PDFs to any other format

Nevertheless it can be used as a part of such tools.

Features
========

* Python 3.6+
* Follows `PDF-1.7 specification <https://www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/PDF32000_2008.pdf>`_
* Lazy objects access allows to process huge PDF documents quite fast
* Allows to extract texts (pure strings and formatted text objects)
* Allows to extract PDF forms data (pure strings and formatted text objects)
* Supports all PDF encodings, CMap, predefined cmaps.
* Allows to extract images and image masks as `Pillow/PIL Images <https://pillow.readthedocs.io/en/stable/reference/Image.html>`_ without loosing any quality
* Allows to access any document objects, resources and extract any data you need (fonts, annotations, metadata, multimedia, etc.)


Installation
============

*pdfreader* can be installed with `pip <http://pypi.python.org/pypi/pip>`_::

  $ python -m pip install pdfreader

Or ``easy_install`` from
`setuptools <http://pypi.python.org/pypi/setuptools>`_::

  $ python -m easy_install pdfreader

You can also download the project source and do::

  $ python setup.py install


Tutorial and Documentation
===========================

`Tutorial, real-life examples and documentation <https://pdfreader.readthedocs.io>`_


Support, Bugs & Feature Requests
============================================

*pdfreader* uses `GitHub issues <https://github.com/maxpmaxp/pdfreader/issues>`_ to keep track of bugs,
feature requests, etc.


Related Projects
================

* `pdfminer <https://github.com/euske/pdfminer>`_ (cool stuff)
* `pyPdf <http://pybrary.net/pyPdf/>`_
* `xpdf <http://www.foolabs.com/xpdf/>`_
* `pdfbox <http://pdfbox.apache.org/>`_
* `mupdf <http://mupdf.com/>`_


References
==========

* `Document management - Potable document format - PDF 1.7 <https://www.adobe.com/content/dam/acom/en/devnet/pdf/pdfs/PDF32000_2008.pdf>`_
* `Adobe CMap and CIDFont Files Specification <https://www.adobe.com/content/dam/acom/en/devnet/font/pdfs/5014.CIDFont_Spec.pdf>`_
* `PostScript Language Reference Manual <https://www-cdf.fnal.gov/offline/PostScript/PLRM2.pdf>`_
* `Adobe CMap resources <https://github.com/adobe-type-tools/cmap-resources>`_
* `Adobe glyph list specification (AGL) <https://github.com/adobe-type-tools/agl-specification>`_