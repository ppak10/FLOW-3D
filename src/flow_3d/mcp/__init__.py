from .__main__ import app
from .resources import register_resources

__all__ = ["app"]

_ = register_resources(app)

