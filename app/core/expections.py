class NotionException(Exception):
    def __init__(
        self, is_ticket=False, code="", message="", redirect_to="", *args, **kwargs
    ):
        self.is_ticket = is_ticket
        self.code = code
        self.message = message
        self.redirect_to = redirect_to
