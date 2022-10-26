from typing import Any
from datetime import datetime, timedelta


class BearerToken:

    def __init__(self):
        pass

    def _verify_issuer(self, issuer: str, payload_issuer: str):
        return issuer == payload_issuer

    def _verify_subject(self, subject: str, payload_subject: str):
        return subject == payload_subject

    def _verify_audience(self, audience: str, payload_audience: str):
        return audience == payload_audience

    def _verify_expiration_time(self,
                                now: float,
                                expiration_time: float):
        return expiration_time <= now

    def _verify_not_before_time(self,
                                now: float,
                                not_before_time: float):
        return not_before_time > now

    def _verify_issued_at_time(self,
                               now: float,
                               issued_at_time: float):
        return issued_at_time > now

    def _verify_claims(self,
                       payload: dict[str, Any],
                       issuer: str,
                       subject: str,
                       audience: str):
        verified_issuer = self._verify_issuer(issuer=issuer,
                                              payload_issuer=payload['issuer'])
        if not verified_issuer:
            return verified_issuer
        verified_subject = self._verify_subject(subject=subject,
                                                payload_subject=payload['subject'])
        if not verified_subject:
            return verified_subject
        verified_audience = self._verify_audience(audience=audience,
                                                  payload_audience=payload['audience'])
        if not verified_audience:
            return verified_audience
        verified_expiration_time = self._verify_expiration_time(now=datetime.utcnow().timestamp(),
                                                                expiration_time=payload['expiration_time'])
        if not verified_expiration_time:
            return verified_expiration_time
        verified_not_before_time = self._verify_not_before_time(now=datetime.utcnow().timestamp(),
                                                                not_before_time=payload['not_before_time'])
        if not verified_not_before_time:
            return verified_not_before_time
        verified_issued_at_time = self._verify_issued_at_time(now=datetime.utcnow().timestamp(),
                                                              issued_at_time=payload['issued_at_time'])
        if not verified_issued_at_time:
            return verified_issued_at_time
        return True

    def _generate_claims(self,
                         issuer: str = None,
                         subject: str = None,
                         audience: str = None,
                         expiration_time: str = None,
                         not_before_time: str = None,
                         issued_at_time: str = None):
        if not expiration_time:
            now = datetime.utcnow()
            expiration_time = (now + timedelta(seconds=7200)).timestamp()

        claims = {'iss': issuer,
                  'sub': subject,
                  'aud': audience,
                  'exp': expiration_time,
                  'nbf': not_before_time,
                  'iat': issued_at_time}

        # now = datetime.utcnow()
        # exp = (now + timedelta(seconds=JWT_TOKEN_EXP)).timestamp()
        # email = values.get("email")
        # claims = {"exp": exp, "email": email}

        return claims

    def encode(self, payload: dict[str, Any]):
        pass

    def verify(self,
               payload: dict[str, Any],
               issuer: str,
               subject: str,
               audience: str):
        pass
