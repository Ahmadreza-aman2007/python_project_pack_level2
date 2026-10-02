import sys
from datetime import datetime
from pathlib import Path

sys.path.append(Path(__file__).parent.parent)
from common.data_manager import DataManager


class Token:
    live_time_for_tokens = 1

    def __init__(
        self,
        token: str,
        created_at: datetime,
        expired_at: datetime,
        owner_code: str | int,
        object_type: str,
    ):
        self.token = token
        self.created_at = created_at
        self.expired_at = expired_at
        self.owner_code = owner_code
        self.is_active = True
        self.object_type = object_type

    @staticmethod
    def build_and_save_Token(personal_code: int | str, cls: object) -> str:
        from secrets import token_urlsafe
        token = token_urlsafe()
        created_at = datetime.now().isoformat()  # noqa: DTZ005
        expired_at = (
            datetime.fromisoformat(created_at)
            + datetime.timedelta(seconds=Token.live_time_for_tokens)
        ).isoformat()
        Token.save_token(
            Token(token, created_at, expired_at, personal_code, cls.__name__)
        )
        return token

    @staticmethod
    def get_tokens() -> list:
        from json import load
        directory_path = DataManager.database_directory
        database_path = directory_path / "token.json"
        if not directory_path.exists():
            directory_path.mkdir()
        if not database_path.exists():
            return []
        with database_path.open("r") as file:
            return load(file)

    @staticmethod
    def save_token(token: "Token"):
        from json import dump
        print(vars(token))
        tokens = Token.get_tokens()
        tokens.append(vars(token))
        print(tokens)
        with (DataManager.database_directory / "token.json").open("w") as file:
            dump(tokens, file, indent=4)

    @staticmethod
    def update_tokens(token: "Token"):
        from json import dump
        tokens = Token.get_tokens()
        for t in tokens:
            if t["token"] == token.token:
                tokens.remove(t)
                tokens.append(vars(token))
                break
        with (DataManager.database_directory / "token.json").open("w") as file:
            dump(tokens, file, indent=4)

    @staticmethod
    def expire_token(token: "Token"):
        token.is_active = False
        Token.update_tokens(token=token)

    @staticmethod
    def delete(token: str):
        from json import dump
        tokens = Token.get_tokens()
        for t in tokens:
            if t["token"] == token:
                tokens.remove(t)
        with (DataManager.database_directory / "token.json").open("w") as file:
            dump(tokens, file, indent=4)

    @staticmethod
    def token_vrification(token: str, personal_code: int | str, cls: str):
        tokens = Token.get_tokens()
        for t in tokens:
            if (
                t["owner_code"] == personal_code
                and t["object_type"] == cls
                and t["token"] == token
            ):
                if (
                    datetime.fromisoformat(t["expired_at"]) < datetime.now()  # noqa: DTZ005
                    or not t["is_active"]
                ):
                    print("your token is expired")
                    Token.delete(token=token)
                    return
                else:
                    return True

        print("token not found")
        return False
