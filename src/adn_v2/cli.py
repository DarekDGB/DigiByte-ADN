from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict

from .engine import ADNEngine


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="adn-v2",
        description="Autonomous Defense Node v2 (reference CLI)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    eval_cmd = sub.add_parser("eval", help="evaluate a single telemetry snapshot")
    eval_cmd.add_argument("--height", type=int, required=True)
    eval_cmd.add_argument("--mempool-size", type=int, required=True)
    eval_cmd.add_argument("--peers", type=int, required=True)

    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    ns = _parse_args(argv or sys.argv[1:])
    engine = ADNEngine(node_id="cli-demo")

    if ns.command == "eval":
        raw: Dict[str, Any] = {
            "height": ns.height,
            "mempool_size": ns.mempool_size,
            "peer_count": ns.peers,
        }
        decision = engine.process_raw_telemetry(raw)
        print(
            json.dumps(
                {
                    "level": decision.level.value,
                    "score": decision.score,
                    "reason": decision.reason,
                    "actions": decision.actions,
                },
                indent=2,
            )
        )
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
