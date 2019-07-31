from chat import TwitterTerminalChat
from unittest import TestCase
from getpass import getuser


class TestTwitterTerminalChat(TestCase):

    path = "C:\\Users\\" + getuser() + "\\PycharmProjects\\twitter_terminal_chat\\account.txt"
    obj = TwitterTerminalChat(account_txt_path=path)

    def test_read_account(self):
        assert self.obj.read_account() is not False


if __name__ == "__main__":
    TestCase()
