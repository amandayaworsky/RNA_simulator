#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main simulator class for generating synthetic RNA sequences."""

from __future__ import annotations

from typing import List, Tuple
import random

from sequence_lib import (
    START_CODON,
    STOP_CODONS,
    generate_random_codon,
    generate_random_sequence,
    get_ambiguity_content,
    get_gc_content,
    write_fasta,
)


class Simulator:
    """Generate RNA sequences with complete or partial ORFs and optional flanks.

    Args:
        num_sequences: Number of sequences to create.
        min_orf_length: Minimum ORF length in nucleotides.
        max_orf_length: Maximum ORF length in nucleotides.
        flanking_probability: Probability of adding flanking regions.
        flanking_length: Length of each flank when added.
        completeness_ratio: Probability of generating a complete ORF.

    Raises:
        ValueError: If any parameter is invalid.
    """

    def __init__(
        self,
        num_sequences: int,
        min_orf_length: int,
        max_orf_length: int,
        flanking_probability: float,
        flanking_length: int,
        completeness_ratio: float,
    ) -> None:
        if num_sequences <= 0:
            raise ValueError("num_sequences must be greater than 0")
        if min_orf_length <= 0 or max_orf_length <= 0:
            raise ValueError("ORF lengths must be greater than 0")
        if min_orf_length > max_orf_length:
            raise ValueError("min_orf_length must be less than or equal to max_orf_length")
        if min_orf_length % 3 != 0 or max_orf_length % 3 != 0:
            raise ValueError("ORF lengths must be multiples of 3")
        if not 0.0 <= flanking_probability <= 1.0:
            raise ValueError("flanking_probability must be between 0 and 1")
        if flanking_length < 0:
            raise ValueError("flanking_length must be non-negative")
        if not 0.0 <= completeness_ratio <= 1.0:
            raise ValueError("completeness_ratio must be between 0 and 1")
        self.num_sequences = num_sequences
        self.min_orf_length = min_orf_length
        self.max_orf_length = max_orf_length
        self.flanking_probability = flanking_probability
        self.flanking_length = flanking_length
        self.completeness_ratio = completeness_ratio

    def generate_orf(self, complete: bool = True) -> str:
        """Generate a complete or partial ORF.

        Args:
            complete: Whether to generate a complete ORF.

        Returns:
            RNA sequence representing the ORF.

        Raises:
            ValueError: If internal generation fails constraints.
        """
        orf_length = random.randrange(self.min_orf_length, self.max_orf_length + 1, 3)
        codon_total = orf_length // 3
        if complete:
            codons = [START_CODON]
            while len(codons) < codon_total - 1:
                codon = generate_random_codon()
                if codon not in STOP_CODONS:
                    codons.append(codon)
            codons.append(random.choice(STOP_CODONS))
            return "".join(codons)
        partial = generate_random_sequence(orf_length)
        if partial.startswith(START_CODON) or partial[-3:] in STOP_CODONS:
            return self.generate_orf(complete=False)
        return partial

    def generate_sequence(self) -> str:
        """Generate one sequence with optional flanking regions.

        Args:
            None.

        Returns:
            Complete simulated RNA sequence.

        Raises:
            None.
        """
        complete = random.random() <= self.completeness_ratio
        core_sequence = self.generate_orf(complete=complete)
        if random.random() > self.flanking_probability:
            return core_sequence
        left_flank = generate_random_sequence(self.flanking_length)
        right_flank = generate_random_sequence(self.flanking_length)
        return f"{left_flank}{core_sequence}{right_flank}"

    def generate_sequences(self) -> List[Tuple[str, str, str]]:
        """Generate all requested sequences with metadata descriptions.

        Args:
            None.

        Returns:
            List of tuples as (sequence_id, description, sequence).

        Raises:
            None.
        """
        records: list[tuple[str, str, str]] = []
        for index in range(1, self.num_sequences + 1):
            sequence = self.generate_sequence()
            complete = sequence.find(START_CODON) != -1 and any(stop in sequence for stop in STOP_CODONS)
            flanked = "yes" if len(sequence) > self.max_orf_length else "yes" if len(sequence) > self.min_orf_length and self.flanking_length > 0 and len(sequence) % 3 != 0 else "no"
            seq_type = "complete" if complete else "partial"
            description = (
                f"length={len(sequence)} gc_content={get_gc_content(sequence)} "
                f"ambiguity={get_ambiguity_content(sequence)} type={seq_type} flanked={flanked}"
            )
            records.append((f"seq_{index:03d}", description, sequence))
        return records

    def save_fasta(self, output_file: str) -> None:
        """Generate records and save them in FASTA format.

        Args:
            output_file: Destination FASTA file path.

        Returns:
            None.

        Raises:
            OSError: If the file cannot be written.
        """
        write_fasta(self.generate_sequences(), output_file)
