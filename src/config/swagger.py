template = {
    "swagger": "2.0",
    "info": {
        "title": "Blog API",
        "description": "API for blog",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "flask@gmail.com",
            "url": "www.twitter.com/flask",
        },
        "termsOfService": "www.twitter.com/flask",
        "version": "1.0"
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "bearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    }
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}
