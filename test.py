#test file
from src import get_config
from src.user import User

# reg = User.register("mukeshmuhi", "mypassword", "mypassword")
# print(reg)

reg = User.login("mukeshmuhi", "mypassword")
print(reg)


