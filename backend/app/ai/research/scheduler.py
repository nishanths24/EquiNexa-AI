import time
from datetime import datetime, timezone
import schedule

from backend.app.ai.research.live_pipeline import LivePredictionPipeline
from backend.app.ai.research.ledger import PredictionLedger
from backend.app.ai.research.outcome_resolver import OutcomeResolver

class AutomationScheduler:
    def __init__(self, pipeline: LivePredictionPipeline, ledger: PredictionLedger, outcome_resolver: OutcomeResolver):
        self.pipeline = pipeline
        self.ledger = ledger
        self.outcome_resolver = outcome_resolver

    def job_generate_predictions(self, tickers):
        now = datetime.now(timezone.utc)
        print(f"[{now}] Running prospective prediction job...")
        # Mock logic
        for ticker in tickers:
            # Here we would fetch df
            # snap = self.pipeline.predict(ticker, "US", df, now)
            # self.ledger.record_prediction(snap)
            pass

    def job_resolve_outcomes(self):
        now = datetime.now(timezone.utc)
        print(f"[{now}] Resolving pending outcomes...")
        self.outcome_resolver.resolve_pending(now)

    def run_local(self, tickers):
        """
        Run once locally.
        """
        self.job_generate_predictions(tickers)
        self.job_resolve_outcomes()

    def start_daemon(self, tickers):
        """
        Start the scheduling daemon.
        """
        schedule.every().day.at("16:30").do(self.job_generate_predictions, tickers=tickers)
        schedule.every().day.at("17:00").do(self.job_resolve_outcomes)
        
        print("Scheduler started. Press Ctrl+C to exit.")
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)
        except KeyboardInterrupt:
            pass
