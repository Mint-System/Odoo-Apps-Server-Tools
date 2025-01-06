.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3

=========================
Server Config Environment
=========================

Define environments for server configurations.

For a detailed documentation have a look at https://www.odoo-wiki.org/server-config-environment.html

Configuration
~~~~~~~~~~~~~

* Connect model to the server config environment:

.. code-block:: python
  
    class GitRepoBranch(models.Model):
        _name = "git.repo.branch"
        _description = "Git Repo Branch"

        field environment_id = Many2one("server.config.environment")

* Define the server environment in the Odoo config:

.. code-block:: toml
  
    [options]
    environment = development

* Use the get active environment to filter records:

.. code-block:: python
  
    environment_id = self.env['server.config.environment'].get_active_environment()
    branch = self.search(['environment_id', '=', environment_id.id)

Maintainer
~~~~~~~~~~

.. image:: https://raw.githubusercontent.com/Mint-System/Wiki/master/assets/mint-system-logo.png
  :target: https://www.mint-system.ch

This module is maintained by Mint System GmbH.

For support and more information, please visit `our Website <https://www.mint-system.ch>`__.
