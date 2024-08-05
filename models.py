from tortoise import Model, fields


class UserModel(Model):
    uid = fields.BigIntField(unique=True)
    password = fields.CharField(max_length=255)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255, null=True)
    username = fields.CharField(max_length=255, null=True)
    language = fields.CharField(max_length=5,)
    jwt_token = fields.CharField(max_length=300, null=True)
    jwt_token_exp = fields.DatetimeField(null=True)
    jwt_refresh_token = fields.CharField(max_length=300, null=True)
    jwt_refresh_token_exp = fields.DatetimeField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    
class ApplicationHistory(Model):
    uid = fields.BigIntField()
    message_id = fields.BigIntField()
    application_id = fields.BigIntField()