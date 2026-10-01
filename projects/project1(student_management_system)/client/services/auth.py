import requests


class EmptyValueError(Exception):
    pass


def login(username: str, password: str):
    if not username or not password:
        print("log:username or password is empty")
        raise EmptyValueError("نام کاربری و رمز عبور نمیتواند خالی باشد")
    response = requests.post(
        "http://127.0.0.1:8080/login", json={"username": username, "password": password}
    )
    print("log: login request sended")
    return response


def register(firstname: str, lastname: str, national_code: str):
    if not (firstname and lastname and national_code):
        print("log:one field in register request is empty")
        raise EmptyValueError("فیلد ها نمیتواند خالی باشد")
    response=requests.post("http://127.0.0.1:8080",json={"firstname":firstname,"lastname":lastname,"national_code":national_code})
    print("log:registration request sended")
    return response