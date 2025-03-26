import gettext
from pathlib import Path

from app.config import settings

file_path = Path(__file__).parent
lang_translations = gettext.translation(
    "base",
    localedir=Path(file_path / ".." / "locale").resolve(),
    languages=[settings.CLIENT_LOCALE],
)
lang_translations.install()

_ = lang_translations.gettext
