from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    alpaca_api_key: str = ""
    alpaca_secret_key: str = ""
    alpaca_base_url: str = "https://paper-api.alpaca.markets"

    llm_provider: str = ""
    llm_api_key: str = ""
    llm_model: str = ""

    aegis_live_trading: bool = False
    aegis_max_position_risk_pct: float = 2.0
    aegis_max_portfolio_risk_pct: float = 10.0
    aegis_max_daily_loss_pct: float = 3.0
    aegis_max_open_positions: int = 5

    @property
    def paper_trading(self) -> bool:
        return not self.aegis_live_trading
