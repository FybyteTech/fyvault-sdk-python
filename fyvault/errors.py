from __future__ import annotations


class FyVaultError(Exception):
    """Base error raised by the FyVault SDK."""

    def __init__(
        self,
        message: str,
        status_code: int = 0,
        code: str = "FYVAULT_ERROR",
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code

    def __repr__(self) -> str:
        return f"FyVaultError({self.message!r}, status_code={self.status_code}, code={self.code!r})"

    @property
    def message(self) -> str:
        return str(self)
