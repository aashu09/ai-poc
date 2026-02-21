from sqlalchemy import (
    String,
    func,
    type_coerce,
    TypeDecorator,
)
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.sql.expression import cast


class PGPString(TypeDecorator):
    impl = BYTEA

    cache_ok = True

    def __init__(self, passphrase):
        super(PGPString, self).__init__()

        self.passphrase = passphrase

    def bind_expression(self, bindvalue):
        # convert the bind's type from PGPString to
        # String, so that it's passed to psycopg2 as is without
        # a dbapi.Binary wrapper
        bindvalue = type_coerce(bindvalue, String)
        return func.pgp_sym_encrypt(bindvalue, self.passphrase)

    def column_expression(self, col):
        return func.pgp_sym_decrypt(cast(col, BYTEA), self.passphrase)