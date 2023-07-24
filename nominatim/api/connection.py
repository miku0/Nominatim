# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of Nominatim. (https://nominatim.org)
#
# Copyright (C) 2023 by the Nominatim developer community.
# For a full list of authors see the git log.
"""
Extended SQLAlchemy connection class that also includes access to the schema.
"""
from typing import cast, Any, Mapping, Sequence, Union, Dict, Optional, Set

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncConnection

from nominatim.typing import SaFromClause
from nominatim.db.sqlalchemy_schema import SearchTables
from nominatim.db.sqlalchemy_types import Geometry
from nominatim.api.logging import log

class SearchConnection:
    """ An extended SQLAlchemy connection class, that also contains
        then table definitions. The underlying asynchronous SQLAlchemy
        connection can be accessed with the 'connection' property.
        The 't' property is the collection of Nominatim tables.
    """

    def __init__(self, conn: AsyncConnection,
                 tables: SearchTables,
                 properties: Dict[str, Any]) -> None:
        self.connection = conn
        self.t = tables # pylint: disable=invalid-name
        self._property_cache = properties
        self._classtables: Optional[Set[str]] = None


    async def scalar(self, sql: sa.sql.base.Executable,
                     params: Union[Mapping[str, Any], None] = None
                    ) -> Any:
        """ Execute a 'scalar()' query on the connection.
        """
        log().sql(self.connection, sql, params)
        return await self.connection.scalar(sql, params)


    async def execute(self, sql: 'sa.Executable',
                      params: Union[Mapping[str, Any], Sequence[Mapping[str, Any]], None] = None
                     ) -> 'sa.Result[Any]':
        """ Execute a 'execute()' query on the connection.
        """
        log().sql(self.connection, sql, params)
        return await self.connection.execute(sql, params)


    async def get_property(self, name: str, cached: bool = True) -> str:
        """ Get a property from Nominatim's property table.

            Property values are normally cached so that they are only
            retrieved from the database when they are queried for the
            first time with this function. Set 'cached' to False to force
            reading the property from the database.

            Raises a ValueError if the property does not exist.
        """
        if name.startswith('DB:'):
            raise ValueError(f"Illegal property value '{name}'.")

        if cached and name in self._property_cache:
            return cast(str, self._property_cache[name])

        sql = sa.select(self.t.properties.c.value)\
            .where(self.t.properties.c.property == name)
        value = await self.connection.scalar(sql)

        if value is None:
            raise ValueError(f"Property '{name}' not found in database.")

        self._property_cache[name] = cast(str, value)

        return cast(str, value)


    async def get_db_property(self, name: str) -> Any:
        """ Get a setting from the database. At the moment, only
            'server_version', the version of the database software, can
            be retrieved with this function.

            Raises a ValueError if the property does not exist.
        """
        if name != 'server_version':
            raise ValueError(f"DB setting '{name}' not found in database.")

        return self._property_cache['DB:server_version']


    async def get_class_table(self, cls: str, typ: str) -> Optional[SaFromClause]:
        """ Lookup up if there is a classtype table for the given category
            and return a SQLAlchemy table for it, if it exists.
        """
        if self._classtables is None:
            res = await self.execute(sa.text("""SELECT tablename FROM pg_tables
                                                WHERE tablename LIKE 'place_classtype_%'
                                             """))
            self._classtables = {r[0] for r in res}

        tablename = f"place_classtype_{cls}_{typ}"

        if tablename not in self._classtables:
            return None

        if tablename in self.t.meta.tables:
            return self.t.meta.tables[tablename]

        return sa.Table(tablename, self.t.meta,
                        sa.Column('place_id', sa.BigInteger),
                        sa.Column('centroid', Geometry))
