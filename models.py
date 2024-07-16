from tortoise import Model, fields


class UserModel(Model):
    uid = fields.BigIntField(unique=True)
    