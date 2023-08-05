#! /usr/bin/env python3

"""Assort phage protein sequences into phamilies using MMseqs2."""

import sys
import argparse
import pathlib
import datetime
import shutil

from phamerate.clustalo import clustalo_align
from phamerate.parallelize import CPUS, parallelize
from phamerate.utility import *

# Defaults parameters
TMP_DIR = pathlib.Path("/tmp/phamerate")

CM, S = 0, 4.0                  # --cluster-mode, -s
M, C, E = 0.3, 0.85, 0.001      # --min-seq-id, -c, -e
HM, HC, HE = 0.25, 0.5, 0.001   # --min-seq-id, -c/--cov, -e/--e-profile

EPILOG = """
Steinegger M. and Soeding J. MMseqs2 enables sensitive protein
sequence searching for the analysis of massive data sets. Nature
Biotechnology, 2017. doi: 10.1038/nbt.3988"""


def parse_args():
    """
    Parse command line arguments

    :return: parsed_args
    """
    p = argparse.ArgumentParser(description=__doc__, prog="phamerate",
                                epilog=EPILOG)

    p.add_argument("infile", nargs="+", type=pathlib.Path,
                   help="path to input file(s) in FASTA format")

    mmseqs_args = p.add_argument_group("mmseqs arguments")
    mmseqs_args.add_argument("--cluster-mode", type=int,
                             default=CM, metavar='',
                             help=f"clustering algorithm [default: {CM}]")
    mmseqs_args.add_argument("--sensitivity", type=float,
                             default=S, metavar='',
                             help=f"sensitivity: 1.0 favors speed, 7.5 favors "
                                  f"sensitivity [default: {S}]")
    mmseqs_args.add_argument("--identity", type=float,
                             default=M, metavar='',
                             help=f"percent identity for sequence-sequence "
                                  f"clustering [default: {M}]")
    mmseqs_args.add_argument("--coverage", type=float,
                             default=C, metavar='',
                             help=f"percent coverage for sequence-sequence "
                                  f"clustering [default: {C}]")
    mmseqs_args.add_argument("--evalue", type=float,
                             default=E, metavar='',
                             help=f"E-value threshold for sequence-sequence "
                                  f"clustering [default: {E}]")
    mmseqs_args.add_argument("--no-hmm", action="store_true",
                             help="skip HMM clustering")
    mmseqs_args.add_argument("--hmm-identity", type=float,
                             default=HM, metavar='',
                             help=f"percent identity for consensus-HMM "
                                  f"clustering [default: {HM}]")
    mmseqs_args.add_argument("--hmm-coverage", type=float,
                             default=HC, metavar='',
                             help=f"percent coverage for consensus-HMM "
                                  f"clustering [default: {HC}]")
    mmseqs_args.add_argument("--hmm-evalue", type=float,
                             default=HE, metavar='',
                             help=f"E-value threshold for consensus-HMM "
                                  f"clustering [default: {HE}]")

    p.add_argument("-c", "--cpus", type=int, default=CPUS, metavar='',
                   help=f"number of threads to use [default: {CPUS}]")
    p.add_argument("-v", "--verbose", action="store_true",
                   help="print progress messages")
    p.add_argument("-o", "--outdir", default=pathlib.Path().cwd(),
                   type=pathlib.Path, metavar='',
                   help=f"path to directory where output files should go "
                        f"[default: {str(pathlib.Path().cwd())}]")
    p.add_argument("-t", "--tmpdir", default=TMP_DIR,
                   type=pathlib.Path, metavar='',
                   help=f"path where temporary file I/O should occur "
                        f"[default: {str(TMP_DIR)}]")
    p.add_argument("-a", "--align-phams", action="store_true",
                   help="use Clustal Omega to align phams (this could take "
                        "awhile...)")

    return p.parse_args()


def main():
    args = parse_args()

    infiles = args.infile

    outdir = args.outdir
    if not outdir.is_dir():
        outdir.mkdir(parents=True)

    tmpdir = args.tmpdir
    if tmpdir.is_dir():
        shutil.rmtree(tmpdir)
    tmpdir.mkdir(parents=True)

    verbose = args.verbose
    cpus = args.cpus
    align = args.align_phams

    # Set up MMseqs2 parameters
    first_iter_params = (args.cluster_mode, args.sensitivity, args.identity,
                         args.coverage, args.evalue)
    second_iter_params = (args.cluster_mode, args.sensitivity,
                          args.hmm_identity, args.hmm_coverage, args.hmm_evalue)

    # Read the translations in from files
    database = create_database(infiles)

    if verbose:
        print(f"Found {len(database)} translations in {len(infiles)} files...")

    # Perform pham assembly
    phams = assemble_phams(database, first_iter_params, second_iter_params,
                           verbose=verbose, threads=cpus,
                           skip_hmm=args.no_hmm, tmp_dir=tmpdir)

    if verbose:
        print(f"Found {len(phams)} phamilies in dataset...")

    fasta_dir = outdir.joinpath("phamily_fastas")
    if not fasta_dir.is_dir():
        fasta_dir.mkdir()

    for i, pham in enumerate(phams):
        fasta_file = fasta_dir.joinpath(f"pham_{i + 1}.faa")
        with open(fasta_file, "w") as fh:
            fh.write(str(pham))

    if align:
        if verbose:
            print("Aligning phams with Clustal Omega...")

        align_dir = outdir.joinpath("phamily_aligns")
        if not align_dir.is_dir():
            align_dir.mkdir(parents=False)

        jobs = [(x, align_dir) for x in fasta_dir.iterdir()]
        parallelize(jobs, cpus, clustalo_align, verbose)

    # TODO: pan-genome style analyses, à la Roary gene_presence_absence.csv


if __name__ == "__main__":
    # Invoke the help menu if phamerate was run without args
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    main()
