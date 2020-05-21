 #!/usr/bin/env python3

import argparse ## https://docs.python.org/3/library/argparse.html#module-argparse
import os
import sys
import XICRA

## initiate parser
parser = argparse.ArgumentParser(
    prog='XICRA',
    description='Small RNA (sRNA) pipeline for...'
  	##,epilog="(c) 2019. Jose F. Sanchez and Lauro Sumoy."
)
subparsers = parser.add_subparsers(title='Available modules', help='', metavar='')

## help options list
help_options = ('--help_format',
				'--help_project',
				'--help_trimm_adapters',
                '--help_join_reads',
                '--help_miRNA',
                '--help_RNAbiotype',
				'--help_multiqc')

## space
#subparser_space = subparsers.add_parser(' ', help='')

#########################
#### Prepare samples ####
#########################

##--------------------------- prepareSamples ----------------- ##
subparser_prep = subparsers.add_parser(
    'prep',
    help='Prepares FASTQ files from samples',
    description='This module prepares fastq files from a sequencing run. It could renamed, copy, link or merge them when multiples files have been generated for the same sample e.g different lanes. It concatenates these files according the common identifier and generates a unique file, one per paired-read if necessary',
)

in_out_group_prep = subparser_prep.add_argument_group("Input/Output")
in_out_group_prep.add_argument("--input", help="Folder containing fastq files. Files could be .fastq/.fq/ or fastq.gz/.fq.gz. All files would be retrieved.", required= not any(elem in help_options for elem in sys.argv))
in_out_group_prep.add_argument("--output_folder", help="Output folder. Name for the project folder.", required= not any(elem in help_options for elem in sys.argv))
in_out_group_prep.add_argument("--single_end", action="store_true", help="Single end files [Default OFF]. Default mode is paired-end.")
in_out_group_prep.add_argument("--batch", action="store_true", help="Provide this option if input is a file containing multiple paths instead a path.")
in_out_group_prep.add_argument("--in_sample", help="File containing a list of samples to include (one per line) from input folder(s) [Default OFF].")
in_out_group_prep.add_argument("--ex_sample", help="File containing a list of samples to exclude (one per line) from input folder(s) [Default OFF].")
in_out_group_prep.add_argument("--detached", help="Isolated mode. No project folder initiated for further steps [Default OFF].")

options_group_prep = subparser_prep.add_argument_group("Options")
options_group_prep.add_argument("--threads", type=int, help="Number of CPUs to use [Default: 2].", default=2)
options_group_prep.add_argument("--copy", action="store_true", help="Instead of generating symbolic links, copy files into output folder. [Default OFF].")
options_group_prep.add_argument("--merge", action="store_true", help="Merges FASTQ files for the same sample [Default OFF].")
options_group_prep.add_argument("--merge-by-lane", action="store_true", help="Merges FASTQ files for the same sample by lane (Technical replicates) [Default OFF].")
options_group_prep.add_argument("--rename", help="File containing original name and final name for each sample separated by comma. No need to provide a name for each pair if paired-end files. If provided with option '--merge', the merge files would be renamed accordingly.")
options_group_prep.add_argument("--include_lane", action="store_true", help="Include the lane tag (*L00X*) in the sample name. See --help_format for additional details [Default OFF]")

info_group_prep = subparser_prep.add_argument_group("Additional information")
info_group_prep.add_argument("--help_format", action="store_true", help="Show additional help on name format for files.")
info_group_prep.add_argument("--help_project", action="store_true", help="Show additional help on the project scheme.")
info_group_prep.add_argument("--debug", action="store_true", help="Show additional message for debugging purposes.")

subparser_prep.set_defaults(func=XICRA.modules.prep.run_prep)
##-------------------------------------------------------------##


##--------------------------- QC ------------------------- ##
subparser_qc = subparsers.add_parser(
    'QC',
    help='Quality check for samples',
    description='This module calls different quality check programs attending the input provided.',
)
in_out_group_qc = subparser_qc.add_argument_group("Input/Output")
in_out_group_qc.add_argument("--input", help="Folder containing input. Project or raw reads, assembly or annotation fasta files according to mode option provided.", required= not any(elem in help_options for elem in sys.argv))
in_out_group_qc.add_argument("--output_folder", help="Output folder. Required if '--detached' mode. Under '--project' mode, information will be stored following a designed scheme. See instructions for further details", required = '--detached' in sys.argv)
in_out_group_qc.add_argument("--batch", action="store_true", help="Provide this option if input is a file containing multiple paths instead a path.")
in_out_group_qc.add_argument("--in_sample", help="File containing a list of samples to include (one per line) from input folder(s) [Default OFF].")
in_out_group_qc.add_argument("--ex_sample", help="File containing a list of samples to exclude (one per line) from input folder(s) [Default OFF].")
in_out_group_qc.add_argument("--detached", action="store_true", help="Isolated mode. --input is a folder containing samples, contigs or protein sequences. Provide a unique path o several using --batch option")

exclusive_group_qc_name = subparser_qc.add_argument_group("Options")
exclusive_group_qc = exclusive_group_qc_name.add_mutually_exclusive_group(required= not any(elem in help_options for elem in sys.argv))
exclusive_group_qc.add_argument("--raw_reads", action="store_true",  help="Check quality for each sample using FASTQC analysis. Input: reads (fastq/fq). See --help_format for further details.")
##exclusive_group_qc.add_argument("--alignment", action="store_true",  help="Check quality for each sample using FASTQC analysis. Input: reads (fastq/fq). See --help_format for further details.")

options_group_qc = subparser_qc.add_argument_group("Configuration")
options_group_qc.add_argument("--single_end", action="store_true", help="Single end files [Default OFF]. Default mode is paired-end. Only applicable if --raw_reads option.")
options_group_qc.add_argument("--skip_report", action="store_true", help="Do not report statistics using MultiQC report module [Default OFF]")
options_group_qc.add_argument("--threads", type=int, help="Number of CPUs to use [Default: 2].", default=2)

info_group_qc = subparser_qc.add_argument_group("Additional information")
info_group_qc.add_argument("--help_format", action="store_true", help="Show additional help on name format for files.")
info_group_qc.add_argument("--help_project", action="store_true", help="Show additional help on the project scheme.")
info_group_qc.add_argument("--help_multiqc", action="store_true", help="Show additional help on the multiQC module.")
info_group_qc.add_argument("--debug", action="store_true", help="Show additional message for debugging purposes.")
subparser_qc.set_defaults(func=XICRA.modules.qc.run_QC)
##-------------------------------------------------------------##

##------------------------------ trimm ----------------------- ##
subparser_trimm = subparsers.add_parser(
    'trimm',
    help='Trimms sequencing adapters.',
    description='This module trimms sequencing adapters that could be present in next generation sequencing files',
)
in_out_group_trimm = subparser_trimm.add_argument_group("Input/Output")
in_out_group_trimm.add_argument("--input", help="Folder containing a project or reads, according to the mode selected. Files could be .fastq/.fq/ or fastq.gz/.fq.gz. See --help_format for additional details.", required= not any(elem in help_options for elem in sys.argv))
in_out_group_trimm.add_argument("--output_folder", help="Output folder.", required = '--detached' in sys.argv)
in_out_group_trimm.add_argument("--single_end", action="store_true", help="Single end files [Default OFF]. Default mode is paired-end.")
in_out_group_trimm.add_argument("--batch", action="store_true", help="Provide this option if input is a file containing multiple paths instead a path.")
in_out_group_trimm.add_argument("--in_sample", help="File containing a list of samples to include (one per line) from input folder(s) [Default OFF].")
in_out_group_trimm.add_argument("--ex_sample", help="File containing a list of samples to exclude (one per line) from input folder(s) [Default OFF].")
in_out_group_trimm.add_argument("--detached", action="store_true", help="Isolated mode. --input is a folder containing fastq reads. Provide a unique path o several using --batch option")

options_group_trimm = subparser_trimm.add_argument_group("Options")
options_group_trimm.add_argument("--skip_report", action="store_true", help="Do not report statistics using MultiQC report module [Default OFF]. See details in --help_multiqc")
options_group_trimm.add_argument("--adapters", help="Adapter sequences to use for the trimming process. See --help_trimm_adapters for further information.")
options_group_trimm.add_argument("--threads", type=int, help="Number of CPUs to use [Default: 2].", default=2)

info_group_trimm = subparser_trimm.add_argument_group("Additional information")
info_group_trimm.add_argument("--help_format", action="store_true", help="Show additional help on name format for files.")
info_group_trimm.add_argument("--help_trimm_adapters", action="store_true", help="Show additional information on trimm adapters.")
info_group_trimm.add_argument("--help_project", action="store_true", help="Show additional help on the project scheme.")
info_group_trimm.add_argument("--help_multiqc", action="store_true", help="Show additional help on the multiQC module.")
info_group_trimm.add_argument("--debug", action="store_true", help="Show additional message for debugging purposes.")

subparser_trimm.set_defaults(func=XICRA.modules.trimm.run_trimm)
##-------------------------------------------------------------##

##------------------------------ join ----------------------- ##
subparser_join = subparsers.add_parser(
    'join',
    help='Joins paired-end reads.',
    description='This module joins sequencing reads (paired-end)',
)
in_out_group_join = subparser_join.add_argument_group("Input/Output")
in_out_group_join.add_argument("--input", help="Folder containing a project or reads, according to the mode selected. Files could be .fastq/.fq/ or fastq.gz/.fq.gz. See --help_format for additional details.", required= not any(elem in help_options for elem in sys.argv))
in_out_group_join.add_argument("--output_folder", help="Output folder.", required = '--detached' in sys.argv)
in_out_group_join.add_argument("--single_end", action="store_true", help="Single end files [Default OFF]. Default mode is paired-end.")
in_out_group_join.add_argument("--batch", action="store_true", help="Provide this option if input is a file containing multiple paths instead a path.")
in_out_group_join.add_argument("--in_sample", help="File containing a list of samples to include (one per line) from input folder(s) [Default OFF].")
in_out_group_join.add_argument("--ex_sample", help="File containing a list of samples to exclude (one per line) from input folder(s) [Default OFF].")
in_out_group_join.add_argument("--detached", action="store_true", help="Isolated mode. --input is a folder containing fastq reads. Provide a unique path o several using --batch option")

options_group_join = subparser_join.add_argument_group("Options")
options_group_join.add_argument("--threads", type=int, help="Number of CPUs to use [Default: 2].", default=2)
options_group_join.add_argument("--perc_diff", type=int, help="Percentage difference for fastqjoin [Default: 8].")


info_group_join = subparser_join.add_argument_group("Additional information")
info_group_join.add_argument("--help_format", action="store_true", help="Show additional help on name format for files.")
info_group_join.add_argument("--help_project", action="store_true", help="Show additional help on the project scheme.")
info_group_join.add_argument("--help_join_reads", action="store_true", help="Show additional help on the join paired-end reads process.")
info_group_join.add_argument("--debug", action="store_true", help="Show additional message for debugging purposes.")

subparser_join.set_defaults(func=XICRA.modules.join.run_join)
##-------------------------------------------------------------##

## space
subparser_space = subparsers.add_parser(' ', help='')

##------------------------------ RNAbiotype ----------------------- ##
subparser_RNAbiotype = subparsers.add_parser(
    'biotype',
    help='RNAbiotype analysis.',
    description='This module generates a RNA biotype analysis',
)
in_out_group_RNAbiotype = subparser_RNAbiotype.add_argument_group("Input/Output")
in_out_group_RNAbiotype.add_argument("--input", help="Folder containing a project or reads, according to the mode selected. Files could be .fastq/.fq/ or fastq.gz/.fq.gz. See --help_format for additional details.", required= not any(elem in help_options for elem in sys.argv))
in_out_group_RNAbiotype.add_argument("--output_folder", help="Output folder.", required = '--detached' in sys.argv)
in_out_group_RNAbiotype.add_argument("--single_end", action="store_true", help="Single end files [Default OFF]. Default mode is paired-end.")
in_out_group_RNAbiotype.add_argument("--batch", action="store_true", help="Provide this option if input is a file containing multiple paths instead a path.")
in_out_group_RNAbiotype.add_argument("--in_sample", help="File containing a list of samples to include (one per line) from input folder(s) [Default OFF].")
in_out_group_RNAbiotype.add_argument("--ex_sample", help="File containing a list of samples to exclude (one per line) from input folder(s) [Default OFF].")
in_out_group_RNAbiotype.add_argument("--detached", action="store_true", help="Isolated mode. --input is a folder containing fastq reads. Provide a unique path o several using --batch option")

options_group_RNAbiotype = subparser_RNAbiotype.add_argument_group("Options")
options_group_RNAbiotype.add_argument("--threads", type=int, help="Number of CPUs to use [Default: 2].", default=2)
options_group_RNAbiotype.add_argument("--perc_diff", type=int, help="Percentage difference for fastqRNAbiotype [Default: 8].")

info_group_RNAbiotype = subparser_RNAbiotype.add_argument_group("Additional information")
info_group_RNAbiotype.add_argument("--help_format", action="store_true", help="Show additional help on name format for files.")
info_group_RNAbiotype.add_argument("--help_project", action="store_true", help="Show additional help on the project scheme.")
info_group_RNAbiotype.add_argument("--help_RNAbiotype", action="store_true", help="Show additional help on the RNAbiotype paired-end reads process.")
info_group_RNAbiotype.add_argument("--debug", action="store_true", help="Show additional message for debugging purposes.")

subparser_RNAbiotype.set_defaults(func=XICRA.modules.biotype.run_biotype)
##-------------------------------------------------------------##

## space
subparser_space = subparsers.add_parser(' ', help='')

##------------------------------ miRNA ----------------------- ##
subparser_miRNA = subparsers.add_parser(
    'miRNA',
    help='miRNA analysis.',
    description='This module generates a miRNA analysis',
)
in_out_group_miRNA = subparser_miRNA.add_argument_group("Input/Output")
in_out_group_miRNA.add_argument("--input", help="Folder containing a project or reads, according to the mode selected. Files could be .fastq/.fq/ or fastq.gz/.fq.gz. See --help_format for additional details.", required= not any(elem in help_options for elem in sys.argv))
in_out_group_miRNA.add_argument("--output_folder", help="Output folder.", required = '--detached' in sys.argv)
in_out_group_miRNA.add_argument("--single_end", action="store_true", help="Single end files [Default OFF]. Default mode is paired-end.")
in_out_group_miRNA.add_argument("--batch", action="store_true", help="Provide this option if input is a file containing multiple paths instead a path.")
in_out_group_miRNA.add_argument("--in_sample", help="File containing a list of samples to include (one per line) from input folder(s) [Default OFF].")
in_out_group_miRNA.add_argument("--ex_sample", help="File containing a list of samples to exclude (one per line) from input folder(s) [Default OFF].")
in_out_group_miRNA.add_argument("--detached", action="store_true", help="Isolated mode. --input is a folder containing fastq reads. Provide a unique path o several using --batch option")

options_group_miRNA = subparser_miRNA.add_argument_group("Options")
options_group_miRNA.add_argument("--threads", type=int, help="Number of CPUs to use [Default: 2].", default=2)
#options_group_miRNA.add_argument("--species", type=int, help="Species tag ID [Default: hsa (Homo sapiens)].", default=2)
##options_group_miRNA.add_argument("--sRNAbench_options", type=int, help="Additional sRNAbench options.")
##options_group_miRNA.add_argument("--miRTop_options", type=int, help="Additional miRTop options.")

info_group_miRNA = subparser_miRNA.add_argument_group("Additional information")
info_group_miRNA.add_argument("--help_format", action="store_true", help="Show additional help on name format for files.")
info_group_miRNA.add_argument("--help_project", action="store_true", help="Show additional help on the project scheme.")
info_group_miRNA.add_argument("--help_miRNA", action="store_true", help="Show additional help on the miRNA paired-end reads process.")
info_group_miRNA.add_argument("--debug", action="store_true", help="Show additional message for debugging purposes.")

subparser_miRNA.set_defaults(func=XICRA.modules.miRNA.run_miRNA)
##-------------------------------------------------------------##

##------------------------------ tRF ----------------------- ##
##subparser_tRF = subparsers.add_parser(
##    'tRF',
##    help='tRF analysis.',
##    description='This module generates a tRF analysis',
##)
##-------------------------------------------------------------##

##------------------------------ piRNA ----------------------- ##
##subparser_piRNA = subparsers.add_parser(
##    'piRNA',
##    help='piRNA analysis.',
##    description='This module generates a piRNA analysis',
##)
##-------------------------------------------------------------##

## space
subparser_space = subparsers.add_parser(' ', help='')

##--------------------------- citation ------------------------##
subparser_citation = subparsers.add_parser(
    'citation',
    help='Packages & software citations.',
    description='This code prints an index of citation for the different packages and other softwares employed here',
)
subparser_citation.add_argument("option", help="Print only this pipeline citation or all packages references.", choices=['only','all'])
subparser_citation.set_defaults(func=XICRA.modules.citation.run)

#####
args = parser.parse_args()
if hasattr(args, 'func'):
    args.func(args)
else:
    parser.print_help()
