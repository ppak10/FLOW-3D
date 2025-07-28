from .__main__ import app
from .version import register_version

__all__ = ["app"]

_ = register_version(app)

if __name__ == "__main__":
    app()

