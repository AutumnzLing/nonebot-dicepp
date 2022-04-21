from git import InvalidGitRepositoryError, NoSuchPathError, GitCommandError

import utils
from utils.logger import dice_log

IS_NEWEST = False


def is_network_error(err_str: str) -> bool:
    return "errno 10054" in err_str or "Timed out" in err_str or "Could not resolve host" in err_str


class GitRepository(object):
    """
    git仓库管理
    """

    def __init__(self, local_path, repo_url, update_source):
        try:
            import nonebot
            import openpyxl
            import rsa
            import yaml
            import os
            import git
        except ImportError as e:
            raise AssertionError(f"当前Python环境缺少必要库\n{e}")

        try:
            assert git.GIT_OK
        except AssertionError:
            git_path = os.path.abspath("../PortableGit/bin/git.exe")
            assert os.path.exists(git_path)
            dice_log(f"找不到系统已安装的Git工具, 使用PortableGit: {git_path}")
            git.refresh(git_path)
        assert git.GIT_OK, "Git不可用..."
        self.local_path = local_path
        self.repo_url = repo_url
        self.update_source = update_source
        self.repo = self.get_git_repo()

    def is_dirty_check(self) -> str:
        if self.repo.is_dirty() and self.repo.head.name == "HEAD" and self.repo.remote().name == "origin":
            return "检测到dicepp源码被修改。若需清除该修改，请键入 .update 初始化 以清除其它更改。"

    def update(self):
        global IS_NEWEST
        if IS_NEWEST:
            return "已是最新。"
        try:
            master = self.repo.heads.master
        except Exception as e:
            return e
        try:
            other = self.repo.create_head("other", "head")
        except Exception as e:
            return e
        try:
            other.checkout()
        except git.exc.CheckoutError as e:
            return e
        try:
            self.repo.remote().fetch()
        except ValueError as e:
            return e
        except GitCommandError as e:
            if e.stderr and is_network_error(e.stderr):
                return "网络连接异常, 请确认没有开启VPN或代理服务, 并再次重试"
            return e
        try:
            master.checkout()
        except git.exc.CheckoutError as e:
            return e
        try:
            self.repo.index.merge_tree(other)
        except GitCommandError as e:
            return e
        try:
            other.delete(self.repo, other)
        except Exception as e:
            utils.logger.dice_log(e)
            return "更新失败：", e
        return "更新完成，请输入.m reboot重启bot以应用更新。"

    def get_update(self):
        global IS_NEWEST
        try:
            c = self.repo.git.log("master..origin/master", "-1", "--pretty={format:%H,%s}")
        except Exception as e:
            return "检查更新失败。原因:", e
        if c:
            IS_NEWEST = False
            return "检测到更新，内容如下", c
        IS_NEWEST = True
        return "已是最新。"

    def refresh(self):
        try:
            self.repo.git.refresh()
        except Exception as e:
            return "初始化代码失败：", e
        return "已成功初始化dicepp代码。"

    def get_git_repo(self):
        try:
            git_repo = git.Repo(self.local_path)
        except InvalidGitRepositoryError as e:
            return "git仓库初始化失败", e
        except NoSuchPathError as e:
            return "git仓库初始化失败", e
        return git_repo


if __name__ == "__main__":
    import os
    import git

    test = GitRepository(r"D:/tmp/dicepp", "https://gitee.com/pear_studio/nonebot-dicepp.git", "gitee")
    test.get_update()
    test.update()
