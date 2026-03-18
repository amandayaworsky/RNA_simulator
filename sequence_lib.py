#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reusable RNA sequence utility functions for the simulator project."""

from __future__ import annotations

from typing import List, Tuple
import random

RNA_BASES: tuple[str, ...] = ("A", "C", "G", "U")
START_CODON: str = "AUG"
STOP_CODONS: tuple[str, ...] = ("UAA", "UAG", "UGA")
IUPAC_AMBIGUOUS: set[str] = {"R", "Y", "S", "W", "K", "M", "B", "D", "H", "V", "N"}
VALID_CODES: set[str] = set(RNA_BASES) | IUPAC_AMBIGUOUS


def _validate_sequence(sequence: str) -> str:
    """Validate and normalize an RNA sequence.

    Args:
        sequence: Input RNA sequence.

    Returns:
        The uppercase sequence.

    Raises:
        ValueError: If the sequence is empty or contains invalid symbols.

    Example:
        >>> _validate_sequence("augc")
        'AUGC'
    """
    normalized = sequence.upper().strip()
    if not normalized:
        raise ValueError("sequence must not be empty")
    if any(base not in VALID_CODES for base in normalized):
        raise ValueError("sequence contains invalid RNA or IUPAC characters")
    return normalized



def get_gc_content(sequence: str) -> float:
    """Calculate GC percentage for an RNA sequence.

    Args:
        sequence: RNA sequence string using uppercase or lowercase letters.

    Returns:
        GC content as a percentage from 0 to 100.

    Raises:
        ValueError: If sequence is empty or contains invalid characters.

    Example:
        >>> get_gc_content("AUGC")
        50.0
    """
    normalized = _validate_sequence(sequence)
    gc_count = sum(1 for base in normalized if base in {"G", "C"})
    return round((gc_count / len(normalized)) * 100, 2)



def get_ambiguity_content(sequence: str) -> float:
    """Calculate ambiguity percentage for an RNA sequence.

    Args:
        sequence: RNA sequence string.

    Returns:
        Ambiguity content as a percentage from 0 to 100.

    Raises:
        ValueError: If sequence is empty or contains invalid characters.

    Example:
        >>> get_ambiguity_content("AUGN")
        25.0
    """
    normalized = _validate_sequence(sequence)
    ambiguous = sum(1 for base in normalized if base in IUPAC_AMBIGUOUS)
    return round((ambiguous / len(normalized)) * 100, 2)



def generate_random_codon() -> str:
    """Generate a random RNA codon.

    Args:
        None.

    Returns:
        A three-nucleotide RNA codon.

    Raises:
        None.

    Example:
        >>> len(generate_random_codon())
        3
    """
    return "".join(random.choice(RNA_BASES) for _ in range(3))



def is_start_codon(codon: str) -> bool:
    """Check whether a codon is the canonical RNA start codon.

    Args:
        codon: Codon string to test.

    Returns:
        True if the codon is AUG, otherwise False.

    Raises:
        ValueError: If codon length is not three or contains invalid symbols.

    Example:
        >>> is_start_codon("AUG")
        True
    """
    normalized = _validate_sequence(codon)
    if len(normalized) != 3:
        raise ValueError("codon must contain exactly 3 nucleotides")
    return normalized == START_CODON



def is_stop_codon(codon: str) -> bool:
    """Check whether a codon is an RNA stop codon.

    Args:
        codon: Codon string to test.

    Returns:
        True if the codon is UAA, UAG, or UGA.

    Raises:
        ValueError: If codon length is not three or contains invalid symbols.

    Example:
        >>> is_stop_codon("UGA")
        True
    """
    normalized = _validate_sequence(codon)
    if len(normalized) != 3:
        raise ValueError("codon must contain exactly 3 nucleotides")
    return normalized in STOP_CODONS



def generate_random_sequence(length: int) -> str:
    """Generate a random RNA sequence of a given length.

    Args:
        length: Number of nucleotides to generate.

    Returns:
        Random RNA sequence of the requested length.

    Raises:
        ValueError: If length is negative.

    Example:
        >>> len(generate_random_sequence(8))
        8
    """
    if length < 0:
        raise ValueError("length must be non-negative")
    return "".join(random.choice(RNA_BASES) for _ in range(length))



def write_fasta(sequences: List[Tuple[str, str, str]], output_file: str) -> None:
    """Write RNA sequences to a FASTA file.

    Args:
        sequences: List of tuples as (sequence_id, description, sequence).
        output_file: Destination file path.

    Returns:
        None.

    Raises:
        ValueError: If no sequences are provided or records are malformed.
        OSError: If the file cannot be written.

    Example:
        >>> write_fasta([("seq1", "demo", "AUGUAA")], "demo.fasta")
    """
    if not sequences:
        raise ValueError("sequences must not be empty")
    lines: list[str] = []
    for record in sequences:
        if len(record) != 3:
            raise ValueError("each FASTA record must contain id, description, and sequence")
        seq_id, description, sequence = record
        normalized = _validate_sequence(sequence)
        lines.append(f">{seq_id} {description}".rstrip())
        lines.extend(normalized[i:i + 60] for i in range(0, len(normalized), 60))
    with open(output_file, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
