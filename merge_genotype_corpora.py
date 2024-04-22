#!/usr/bin/env python3
#//////////////////////////////////////////////////////////////////////////#
#                                                                          #
#   Copyright (C) 2019 by David B. Blumenthal                              #
#                                                                          #
#   This file is part of EpiGEN.                                           #
#                                                                          #
#   EpiGEN is free software: you can redistribute it and/or modify         #
#   it under the terms of the GNU General Public License as published by   #
#   the Free Software Foundation, either version 3 of the License, or      #
#   (at your option) any later version.                                    #
#                                                                          #
#   EpiGEN is distributed in the hope that it will be useful,              #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the           #
#   GNU General Public License for more details.                           #
#                                                                          #
#   You should have received a copy of the GNU General Public License      #
#   along with EpiGEN. If not, see <http://www.gnu.org/licenses/>.         #
#                                                                          #
#//////////////////////////////////////////////////////////////////////////#

"""Run this script to merge pre-computed genotype corpora.

For each HAPMAP3 population and each chromosome, EpiGEN comes with a pre-computed corpus for 10000 individuals.
The corpora for chromosome <CHROM> have corpus ID <CHROM> and can be used by ``simulate_data.py`` right away.
If you want to these or other corpora, run this script.

**Usage**:: 
    
    python3 merge_genotype_corpora.py [required arguments] [optional arguments]

**Requried Arguments:**
    ``--corpus-id CORPUS_ID``
        Description:
            ID of merged genotype corpus.
        Accepted Arguments:
            Non-negative integers. If contained in range(1,23), the pre-computed corpora shipped with EpiGEN are overwritten.
        Effect:
            Together with ``--pop``, this option determines the prefix ``./corpora/<CORPUS_ID>_<POP>`` of the files
            that contain the generated corpus.
    ``--pops POP POP [POP ...]``    
        Description:
            List of HAPMAP3 population codes of the corpora that should be merged. 
            The size must match the size of the argument passed to ``--corpus-ids``.
        Accepted Arguments: 
            ASW, CEU, CEU+TSI, CHD, GIH, JPT+CHB, LWK, MEX, MKK, TSI, and MIX.
        Effect:
            Selects the corpora that should be merged and determines the prefix ``./corpora/<CORPUS_ID>_<POP>`` of the files
            that contain the generated corpus. If the list passed to this argument contains only one population code,
            ``<POP>`` is the set to this code. Otherwise, ``<POP>`` is set to ``MIX``. 
    ``--corpus-ids CORPUS_ID CORPUS_ID [CORPUS_ID ...]``
        Description:
            The IDs of the corpora that should be merged.
        Accepted Arguments:
            Lists of non-negative integers of size at least 2.
            The size must match the size of the argument passed to ``--pops``.
        Effect:
            Selects the corpora that should be merged.
    ``--append APPEND``
        Description:
            The axis along which the corpora should be merged.
        Accepted Arguments:
            "SNPS" or "INDS". 
        Effect:
            Set to "SNPS" to append the SNPs and to "INDS" to append the individuals.

**Optional Arguments:**
    ``--compress``
        Description:
            Compress the generated output files.
        Accepted Arguments:
            None.
        Effect:
            Determines the suffix ``<SUFFIX>`` of the generated files. If provided, ``<SUFFIX>`` is set to ``json.bz2``.
            Otherwise, it is set to ``json``.
    ``-h, --help``
        Effect:
            Show help message and exit.
            
**Output:**
    *Genotype Data:*
        File: 
            ``./corpora/<CORPUS_ID>_<POP>_genotype.<SUFFIX>``
        Content and Format: 
            (Compressed) JSON file of the form ``[[G_0_0, ..., G_0_<INDS-1>], ..., [G_<SNPS-1>_0, ..., G_<SNPS-1>_<INDS-1>]]``,
            where ``G_S_I`` encodes the number of minor alleles of the individual with index ``I`` at the SNP with index ``S``.
    *SNPs:*
        File:
            ``./corpora/<CORPUS_ID>_<POP>_snps.<SUFFIX>``
        Content and Format:
            (Compressed) JSON file of the form ``[INFO_0, ..., INFO_<SNPS-1>]``, where ``INFO_S`` contains the following
            information about the SNP with index ``S``: RS identifier, chromosome number, position on chromosome, major allele, minor allele.
    *MAFs:*
        File:
            ``./corpora/<CORPUS_ID>_<POP>_mafs.<SUFFIX>``
        Content and Format:
            (Compressed) JSON file of the form ``[MAF_0, ..., MAF_<SNPS-1>]``, where ``MAF_S`` encodes the MAF of
            the SNP with index ``S``.
    *Cumulative MAF distribution:*
        File: 
            ``./corpora/<CORPUS_ID>_<POP>_cum_mafs.<SUFFIX>``
        Content and Format:
            (Compressed) ordered JSON file of the form ``[[MAF_0, COUNT_0], ..., [MAF_<NMAFS-1>, COUNT_<NMAFS-1>]]``, where ``COUNT_POS`` encodes the 
            number of SNPs is does not exceed ``MAF_POS``.
    *Plot of Cumulative MAF distribution:*
        File: 
            ``./corpora/<CORPUS_ID>_<POP>_cum_mafs.pdf``
        Content and Format:
            Plot of cumulative MAF distribution. Can be used to determine feasible ranges of MAFs passed to the options 
            ``--global-maf-range`` and ``--disease-maf-range`` of the script ``simulate_data.py``.
"""

from utils.genotype_corpus_merger import GenotypeCorpusMerger as GenCorMerge
import utils.argparse_checks as checks
import argparse

def run_script():
    """Runs the script."""
    
    descr = "\n############################################################################\n"
    descr += "#################### EpiGEN - merge_genotype_corpora.py ####################\n"
    descr += "\nRun this script to merge genotype corpora.\n"
    descr += "\nusage: python3 %(prog)s [required arguments] [optional arguments]\n"
    epilo = "The generated data can be found in the ./corpora directory:\n"
    epilo += "Genotype data:\t\t\t./corpora/<CORPUS_ID>_<POP>_genotype.<SUFFIX>\n"
    epilo += "SNPs:\t\t\t\t./corpora/<CORPUS_ID>_<POP>_snps.<SUFFIX>\n"
    epilo += "MAFs:\t\t\t\t./corpora/<CORPUS_ID>_<POP>_mafs.<SUFFIX>\n"
    epilo += "Cumulative MAF distr.:\t\t./corpora/<CORPUS_ID>_<POP>_cum_mafs.<SUFFIX>\n"
    epilo += "Plot of cumulative MAF distr.:\t./corpora/<CORPUS_ID>_<POP>_cum_mafs.pdf\n"
    epilo += "\n############################################################################\n"
    parser = argparse.ArgumentParser(description=descr,formatter_class=argparse.RawTextHelpFormatter, epilog=epilo, usage=argparse.SUPPRESS)
    required_args = parser.add_argument_group("requried arguments")
    required_args.add_argument("--corpus-ids", type=int, nargs="+", required=True, help="IDs of corpora that should be merged.", metavar="CORPUS_ID", action=checks.check_length("--corpus-ids"))
    required_args.add_argument("--corpus-id", type=int, required=True, help="ID of generated corpus.", action=checks.check_non_negative("--corpus-id"))
    required_args.add_argument("--pops", nargs="+", required=True, choices=["ASW","CEU","CEU+TSI","CHD","GIH","JPT+CHB","LWK","MEX","MKK","TSI","MIX"], metavar="POP", help="HAPMAP3 population codes of corpora that should be merged.", action=checks.check_length("--pops"))
    required_args.add_argument("--append", required=True, help="The axis along which the corpora should be merged.", choices=["SNPS","INDS"])
    optional_args = parser.add_argument_group("optional arguments")
    optional_args.add_argument("--compress", help="Compress generated output files.", action="store_true")
    args = parser.parse_args()
    
    print("\n############################################################################")
    print("#################### EpiGEN - merge_genotype_corpora.py ####################\n")
    axis = 0
    if args.append == "INDS":
        axis = 1
    merger = GenCorMerge(args.corpus_ids, args.pops, args.corpus_id, axis, args.compress)
    merger.merge_corpora()
    merger.compute_mafs()
    merger.dump_corpus()
    suffix = "json"
    if args.compress:
        suffix = "json.bz2"
    print("\n----------------------------------------------------------------------------\n")
    print("Finished merging of genotype corpora.")
    print("The generated data can be found in the ./corpora directory:")
    print("Number of SNPs:\t\t\t" + str(merger.num_snps))
    print("Genotype data:\t\t\t./corpora/" + str(args.corpus_id) + "_" + merger.pop + "_genotype." + suffix)
    print("SNPs:\t\t\t\t./corpora/" + str(args.corpus_id) + "_" + merger.pop + "_snps." + suffix)
    print("MAFs:\t\t\t\t./corpora/" + str(args.corpus_id) + "_" + merger.pop + "_mafs." + suffix)
    print("Cumulative MAF distr.:\t\t./corpora/" + str(args.corpus_id) + "_" + merger.pop + "_cum_mafs." + suffix)
    print("Plot of cumulative MAF distr.:\t./corpora/" + str(args.corpus_id) + "_" + merger.pop + "_cum_mafs.pdf")
    
    print("\n############################################################################")
    
if __name__ == "__main__":
    run_script()
