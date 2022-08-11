from marshmallow import Schema, fields


class PostRegisterSchema(Schema):
    title = fields.String(required=True)
    content = fields.String(required=True)


class PostUpdateSchema(Schema):
    title = fields.String(required=True)
    content = fields.String(required=True)


class PostResponseSchema(Schema):
    title = fields.String()
    content = fields.String()
