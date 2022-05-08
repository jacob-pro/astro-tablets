import os
import subprocess


class GitInfo:
    def __init__(self):
        hash = os.getenv("GIT_HASH")
        if hash is not None:
            if len(hash) < 1:
                raise RuntimeError("GIT_HASH must not be empty")
            self.hash = hash
            self.dirty = False
        else:
            self.hash = self.get_hash()
            self.dirty = self.get_dirty()

    @staticmethod
    def get_hash() -> str:
        try:
            return (
                subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
                .decode("utf-8")
                .partition("\n")[0]
            )
        except subprocess.CalledProcessError:
            raise RuntimeError("Failed to get git hash")

    @staticmethod
    def get_dirty() -> bool:
        try:
            subprocess.check_output(
                ["git", "diff", "--exit-code"], stderr=subprocess.PIPE
            )
        except subprocess.CalledProcessError:
            return True
        return False
