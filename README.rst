A simple Tag Bot supporting slash commands with autocompletion

Prerequisites
-------------

Create an sqlite database using the `scheme.sql` file

.. code-block:: sh

    sqlite3 database.db -init scheme.sql ""

Deployment
-------------

- Rename the ``docker-compose.yml.example`` file to ``docker-compose.yml``.
- Update the ``TAG_BOT_TOKEN`` environment variable to use your own discord bot token.
- Update the ``TAG_BOT_DB_FILE_PATH`` environment variable to specify where the database is mounted in the container.
- Update the container volume path accordingly.
- Run ``docker-compose up -d tag_bot``
