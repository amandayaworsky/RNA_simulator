#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Command-line entry point for the RNA sequence simulator."""

from __future__ import annotations

import argparse
import sys

from simulator import Simulator



def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser.

    Args:
        None.

    Returns:
        Configured ArgumentParser instance.

    Raises:
        None.
    """
    parser = argparse.ArgumentParser(description="Generate synthetic RNA sequences in FASTA format.")
    parser.add_argument("-n", "--num-sequences", type=int, default=10, help="Number of sequences to generate.")
    parser.add_argument("-o", "--output", default="sequences.fasta", help="Output FASTA file path.")
    parser.add_argument("--min-length", type=int, default=99, help="Minimum ORF length in nucleotides.")
    parser.add_argument("--max-length", type=int, default=999, help="Maximum ORF length in nucleotides.")
    parser.add_argument("--flanking-prob", type=float, default=0.5, help="Probability of adding flanks.")
    parser.add_argument("--flanking-length", type=int, default=50, help="Length of each flanking region.")
    parser.add_argument("--completeness", type=float, default=0.7, help="Ratio of complete ORFs.")
    return parser



def validate_arguments(args: argparse.Namespace) -> None:
    """Validate parsed command-line arguments.

    Args:
        args: Parsed argparse namespace.

    Returns:
        None.

    Raises:
        ValueError: If any argument violates project constraints.
    """
    if args.num_sequences <= 0:
        raise ValueError("--num-sequences must be greater than 0")
    if args.min_length <= 0 or args.max_length <= 0:
        raise ValueError("--min-length and --max-length must be greater than 0")
    if args.min_length > args.max_length:
        raise ValueError("--min-length cannot be greater than --max-length")
    if args.min_length % 3 != 0 or args.max_length % 3 != 0:
        raise ValueError("--min-length and --max-length must be multiples of 3")
    if not 0.0 <= args.flanking_prob <= 1.0:
        raise ValueError("--flanking-prob must be between 0 and 1")
    if args.flanking_length < 0:
        raise ValueError("--flanking-length must be non-negative")
    if not 0.0 <= args.completeness <= 1.0:
        raise ValueError("--completeness must be between 0 and 1")



def main() -> int:
    """Run the simulator application.

    Args:
        None.

    Returns:
        Exit status code.

    Raises:
        None.
    """
    parser = create_parser()
    try:
        args = parser.parse_args()
        validate_arguments(args)
        simulator = Simulator(
            num_sequences=args.num_sequences,
            min_orf_length=args.min_length,
            max_orf_length=args.max_length,
            flanking_probability=args.flanking_prob,
            flanking_length=args.flanking_length,
            completeness_ratio=args.completeness,
        )
        simulator.save_fasta(args.output)
        sys.stdout.write(f"✓ Successfully generated {args.num_sequences} sequences\n")
        sys.stdout.write(f"✓ Output saved to: {args.output}\n")
        return 0
    except Exception as exc:
        sys.stderr.write(f"Error: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
