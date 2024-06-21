.. image:: https://img.shields.io/badge/licence-GPL--3-blue.svg
    :target: http://www.gnu.org/licenses/gpl-3.0-standalone.html
    :alt: License: GPL-3

========
Url Slug
========

Generate slug from record name for web urls.

For a detailed documentation have a look at https://www.odoo-wiki.org/base-url-slug.html

Configuration
~~~~~~~~~~~~~

* Inherit the slug mixin in your module:

.. code-block:: python
  
  class Tag(models.Model):
      _name = "note.note"
      _inherit = ['mail.thread', 'mail.activity.mixin', 'url_slug.mixin']
      _description = "Note"
      _order = 'sequence, id desc'

Maintainer
~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/Mint-System/Wiki/master/assets/mint-system-logo.png
  :target: https://www.mint-system.ch

This module is maintained by Mint System GmbH.

For support and more information, please visit `our Website <https://www.mint-system.ch>`__.
