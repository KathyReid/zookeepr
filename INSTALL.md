Zookeepr Installation Instructions
==================================

External dependencies
---------------------

 * libpq-dev
 * libpython-dev
 * libxslt1-dev
 * libxml2-dev
 * postgresql
 * python-virtualenv


Creating a development environment
----------------------------------

1. Create a postgresql database for your ZooKeepr instance. The first command creates the database user, the second the database itself, with the zookeepr user as the admin user, and the third assigns a password to the zookeepr user.

    ```
    $ sudo -u postgres createuser --no-createdb --no-createrole --no-superuser zookeepr
    $ sudo -u postgres createdb -O zookeepr zk
    $ sudo -u postgres psql --command "ALTER USER zookeepr with PASSWORD 'zookeepr'"
    ```

2. Create a virtualenv for your ZooKeepr instance.

        ```
        \# using only virtualenv
        $ sudo virtualenv env --no-site-packages
        $ . ./env/bin/activate

        \# using virtualenwrapper
        $ sudo mkvirtualenv zookeepr # --no-site-packages is default
        $ workon zookeepr
        ```

3. Configure the virtual environment.

        ```
        $ sudo cp zkpylons/config/lca_info.py.sample zkpylons/config/lca_info.py
        $ sudo cp development.ini.sample development.ini
        $ sudo python setup.py develop
        ```
    Edit development.ini to set sqlalchemy.url to match your postgresql database.
    _Note: You must set sqlalchemy.url in both the [app:main] and [alembic] sections_

4. Now, we populate database. Run alembic to create and populate the initial database.

        ```
        $ sudo alembic --config development.ini upgrade head
        ```

        WARNING: On a vanilla trunk this does not currently work but there
        is a workaround:

            * Zookeepr is using alembic in a rather unusual way, which leads to
            problems. James has a work-around for this, but it is not currently in
            master and should never be committed to master. The work-around can be
            cherry-picked, commit c3812eb0 from
            https://github.com/iseppi/zookeepr.git on the nasty-db-import-fix
            branch.

            ```
            $ sudo git remote add alembicfix https://github.com/iseppi/zookeepr.git
            $ sudo git fetch alembicfix nasty-db-import-fix
            $ sudo git cherry-pick a641643758d88238e4ada43f873d7b021238debe
            $ sudo alembic --config development.ini upgrade head
            $ sudo alembic --config development.ini stamp 624cf57a935
            ```

            To verify the fix, use the alembic history command and check that the
            head revision is "This revision is a lie and should always be head".

            ```
            $ alembic --config development.ini history
            git reset --hard HEAD^
            ```

            Now, we verify that the revision is no longer present, using the command;

            ```
            $ alembic --config development.ini history
            ```

            The phrase 'This revision is a lie' should *no longer* be present.

5. Run the development server.

        ```
        pserve --reload development.ini
        ```

_NOTE: If you are running MythTV, this can conflict, as MythTV also runs on port 6543. You will need to kill or uninstall MythTV to continue._

You should now have a development instance of ZooKeepr up and running.

Access it at: [http://0.0.0.0:6543](http://0.0.0.0:6543)

*Congratulations*
