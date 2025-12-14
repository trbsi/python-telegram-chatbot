class AgeVerificationValueObject:
    def __init__(
            self,
            session_id: str,
            status: str,
            redirect_url: str
    ) -> None:
        self.session_id = session_id
        self.status = status
        self.redirect_url = redirect_url
