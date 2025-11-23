from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Dict

from .client import ADNClient
from .config import ADNConfig


def _parse_json_arg(value: str) -> Dict[str, Any]:
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise argparse.ArgumentTypeError(f"Invalid JSON: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="ADN v2 reference CLI – evaluate risk and actions.",
    )
    parser.add_argument(
        "--chain",
        type=_parse_json_arg,
        required=True,
        help="JSON dict with chain metrics.",
    )
    parser.add_argument(
        "--sentinel",
        type=_parse_json_arg,
        required=True,
        help="JSON dict with Sentinel AI v2 output.",
    )
    parser.add_argument(
        "--wallet",
        type=_parse_json_arg,
        required=False,
        help="Optional JSON dict with Wallet Guardian aggregate signal.",
    )

    args = parser.parse_args(argv)

    client = ADNClient(config=ADNConfig())
    plan = client.evaluate(args.chain, args.sentinel, args.wallet)

    json.dump(plan, sys.stdout, default=lambda o: o.value if hasattr(o, "value") else o)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
