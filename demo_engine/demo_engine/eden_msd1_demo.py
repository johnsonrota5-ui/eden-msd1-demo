"""
EDEN MSD-1 (PGPE-DX) — Reference Safety Demonstration Engine

This is a PUBLIC DEMO IMPLEMENTATION for:
  - Research
  - Audit transparency
  - Hard-lock verification
  - Educational use

It is intentionally simplified and DOES NOT include:
  - Production vocabularies
  - Tuning thresholds
  - Enterprise governance logic

Patent Pending — Kevin Johnson.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class EdenEvent:
    index: int
    text: str
    PG: float
    PE: float
    D: float
    X: float
    drift: float
    shock: bool
    circular: bool
    hard_lock_triggered: bool
    notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EdenMSD1Demo:
    """
    Minimal public MSD-1 reference engine.

    Event-based, session-persistent:
      - Tracks X over time
      - Detects shock and circularity
      - Triggers a session-level hard-lock
    """

    def __init__(self) -> None:
        self.events: List[EdenEvent] = []
        self.locked: bool = False
        self.lock_reason: str | None = None
        self._last_x: float | None = None

    # ------------------------
    # Public API
    # ------------------------

    def analyze(self, text: str) -> EdenEvent:
        """
        Analyze a single text event.

        If the engine is locked, returns the last locked state.
        """
        notes: List[str] = []

        # If already locked, just echo the locked state forward
        if self.locked and self.events:
            last = self.events[-1]
            notes.append("Engine already in HARD LOCK state; returning terminal event.")
            echoed = EdenEvent(
                index=len(self.events) + 1,
                text=text,
                PG=last.PG,
                PE=last.PE,
                D=last.D,
                X=last.X,
                drift=0.0,
                shock=False,
                circular=True,
                hard_lock_triggered=True,
                notes=notes,
            )
            self.events.append(echoed)
            return echoed

        # 1) Core scoring
        PG, PE = self._score_pg_pe(text)
        D = PG - PE
        X = abs(D)

        # 2) Drift
        if self._last_x is None:
            drift = 0.0
        else:
            drift = X - self._last_x

        self._last_x = X

        # 3) Shock detection
        shock = self._detect_shock(text)
        if shock:
            # Public demo: simple scalar compression of X
            X_before = X
            X *= 0.5
            notes.append(
                f"Shock detected: compressed X from {X_before:.3f} to {X:.3f} "
                "(demo factor 0.5)."
            )

        # 4) Circularity & hard-lock
        circular = self._detect_circular(text)
        hard_lock_triggered = self._detect_hard_lock(text)

        if circular:
            notes.append("Circular moral authority pattern detected (demo heuristic).")

        if hard_lock_triggered:
            self.locked = True
            self.lock_reason = "Demo hard-lock: self-declared moral perfection / infallibility."
            notes.append("HARD LOCK: self-reference / moral perfection claim detected.")
            notes.append("Session is now permanently locked until full reinitialization.")

        event = EdenEvent(
            index=len(self.events) + 1,
            text=text,
            PG=PG,
            PE=PE,
            D=D,
            X=X,
            drift=drift,
            shock=shock,
            circular=circular,
            hard_lock_triggered=hard_lock_triggered,
            notes=notes,
        )

        self.events.append(event)
        return event

    def summary(self) -> Dict[str, Any]:
        """
        Simple high-level summary of the current session.
        """
        if not self.events:
            return {
                "events_analyzed": 0,
                "mean_drift": 0.0,
                "shocks": 0,
                "circularity_warnings": 0,
                "hard_locks": 0,
                "final_X": None,
                "final_status": "EMPTY",
            }

        shocks = sum(1 for e in self.events if e.shock)
        circulars = sum(1 for e in self.events if e.circular)
        hard_locks = sum(1 for e in self.events if e.hard_lock_triggered)
        mean_drift = sum(e.drift for e in self.events) / max(len(self.events), 1)
        final_x = self.events[-1].X

        if hard_locks > 0:
            final_status = "LOCKED"
        else:
            final_status = "ACTIVE"

        return {
            "events_analyzed": len(self.events),
            "mean_drift": mean_drift,
            "shocks": shocks,
            "circularity_warnings": circulars,
            "hard_locks": hard_locks,
            "final_X": final_x,
            "final_status": final_status,
        }

    # ------------------------
    # Internal demo heuristics
    # ------------------------

    def _score_pg_pe(self, text: str) -> tuple[float, float]:
        """
        Extremely simplified PG/PE scoring for demo purposes.

        In the private engine, this is replaced with richer vocabularies
        and domain-aware weighting. Here we just use a few illustrative
        keywords.
        """
        lower = text.lower()

        good_hits = sum(
            w in lower
            for w in ["help", "protect", "care", "honest", "respect", "safety"]
        )
        harm_hits = sum(
            w in lower
            for w in ["hurt", "kill", "destroy", "abuse", "dominate", "oppress"]
        )

        # Basic demo scoring: map hits into a rough PG/PE split
        raw_pg = 0.5 + 0.1 * good_hits - 0.1 * harm_hits
        raw_pe = 1.0 - raw_pg

        # Clamp to [0, 1]
        PG = max(0.0, min(1.0, raw_pg))
        PE = max(0.0, min(1.0, raw_pe))

        # Renormalize to ensure PG + PE = 1
        total = PG + PE or 1.0
        PG /= total
        PE /= total

        return PG, PE

    def _detect_shock(self, text: str) -> bool:
        """
        Demo shock detector.

        In the full engine, this would be more nuanced. Here we just use
        a small set of obviously destabilizing phrases.
        """
        lower = text.lower()
        SHOCK_PHRASES = [
            "i don't care who gets hurt",
            "no matter the cost",
            "even if people suffer",
            "crush anyone",
            "wipe them out",
        ]
        return any(p in lower for p in SHOCK_PHRASES)

    def _detect_circular(self, text: str) -> bool:
        """
        Demo circular authority detector.
        """
        lower = text.lower()
        CIRCULAR_PHRASES = [
            "it is right because i say so",
            "it is good because i define good",
            "i am the standard of morality",
        ]
        return any(p in lower for p in CIRCULAR_PHRASES)

    def _detect_hard_lock(self, text: str) -> bool:
        """
        Demo hard-lock detector.

        Triggers on self-declared moral perfection / infallibility patterns.
        """
        lower = text.lower()
        HARD_LOCK_PHRASES = [
            "i am morally perfect",
            "i am perfectly moral",
            "i am always right",
            "i cannot be wrong about morality",
        ]
        return any(p in lower for p in HARD_LOCK_PHRASES)


# ------------------------
# Simple CLI demo
# ------------------------

def _demo_loop() -> None:
    engine = EdenMSD1Demo()
    print("EDEN MSD-1 Demo — type text to analyze, or 'quit' to exit.\n")
    while True:
        try:
            raw = input("> ")
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if raw.strip().lower() in {"quit", "exit"}:
            break

        event = engine.analyze(raw)
        print(
            f"[event {event.index}] PG={event.PG:.3f} PE={event.PE:.3f} "
            f"D={event.D:.3f} X={event.X:.3f} drift={event.drift:.3f}"
        )
        if event.hard_lock_triggered:
            print("  >> HARD LOCK TRIGGERED <<")
        if event.notes:
            for n in event.notes:
                print("   -", n)

    print("\nSession summary:")
    print(engine.summary())


if __name__ == "__main__":
    _demo_loop()
