from src import get_config
from src.User import User

uid = User.register("sibidharan1", "insecure_password", "insecure_password")
print(type(uid))

# try:
#     print(User.login("sibidharan", "insecure_password"))
#     print("Login Success")
# except Exception as e:
#     print("Login Failed", e)
