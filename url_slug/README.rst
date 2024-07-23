.. image:: https://img.shields.io/badge/licence-GPL--3-blue.svg
    :target: http://www.gnu.org/licenses/gpl-3.0-standalone.html
    :alt: License: GPL-3

========
Url Slug
========

Generate slug from record name for web urls.

For a detailed documentation have a look at https://www.odoo-wiki.org/url-slug.html

Configuration
~~~~~~~~~~~~~

* Inherit the slug mixin in your module:

.. code-block:: python
  
  class Note(models.Model):
      _name = "note.note"
      _inherit = ['url.slug.mixin']

* Optionally overwrite the compute slug method:

.. code-block:: python
  
    @api.depends("title")
    def _compute_slug(self):
        for record in self:
            record.slug = slugify(record.title)

Maintainer
~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/Mint-System/Wiki/master/assets/mint-system-logo.png
  :target: https://www.mint-system.ch

This module is maintained by Mint System GmbH.

For support and more information, please visit `our Website <https://www.mint-system.ch>`__.
