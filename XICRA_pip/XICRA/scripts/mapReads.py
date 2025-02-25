#!/usr/bin/env python3
############################################################
## Jose F. Sanchez                                        ##
## Copyright (C) 2019-2020 Lauro Sumoy Lab, IGTP, Spain   ##
############################################################
## useful imports
import time
import io
import os
import re
import sys
from sys import argv
import subprocess

from HCGB.functions import system_call_functions
from HCGB.functions import files_functions

############################################################
def create_genomeDir(folder, STAR_exe, num_threads, fasta_file, limitGenomeGenerateRAM):
    
    ##
    genomeDir = files_functions.create_subfolder("STAR_index", folder)
    
    cmd_create = "%s --runMode genomeGenerate --limitGenomeGenerateRAM %s --runThreadN %s --genomeDir %s --genomeFastaFiles %s" %(
        STAR_exe, limitGenomeGenerateRAM, num_threads, genomeDir, fasta_file)

    print ('\t+ genomeDir generation for STAR mapping')
    create_code = system_call_functions.system_call(cmd_create, False, True)
    
    if not create_code:
        print ("** ERROR: Some error ocurred during genomeDir creation... **")
        exit()
    
    return (genomeDir)

############################################################
def load_Genome(folder, STAR_exe, genomeDir, num_threads):
    
    ## --genomeLoad LoadAndExit
    Load_folder = files_functions.create_subfolder('LoadMem', folder)
    cmd_LD = "%s --genomeDir %s --runThreadN %s --outFileNamePrefix %s --genomeLoad LoadAndExit" %(
        STAR_exe, genomeDir, num_threads, Load_folder)
    
    print ('\t+ Loading memory for STAR mapping')
    load_code = system_call_functions.system_call(cmd_LD, False, True)
    return (load_code)

############################################################
def remove_Genome(STAR_exe, genomeDir, folder, num_threads):
    
    ## --genomeLoad Remove
    remove_folder = files_functions.create_subfolder('RemoveMem', folder)
    cmd_RM = "%s --genomeDir %s --outFileNamePrefix %s --runThreadN %s --genomeLoad Remove" %(
        STAR_exe, genomeDir, remove_folder, num_threads)
    
    ## send command    
    print ('\t+ Removing memory loaded for STAR mapping')
    remove_code = system_call_functions.system_call(cmd_RM, False, True)
    return (remove_code)

############################################################
def mapReads(option, reads, folder, name, STAR_exe, genomeDir, limitRAM_option, num_threads, Debug):
    """
    Map reads using STAR software. Some parameters are set for small RNA Seq.

    Parameters set according to ENCODE Project directives for small RNAs
    https://www.encodeproject.org/rna-seq/small-rnas/
    
    :param option: If multiple files to map, use loaded genome (LoadAndKeep) if only one map, anything else.
    :param reads: List containing absolute path to reads (SE or PE)
    :param folder: Path for output results
    :param name: Sample name
    :param STAR_exe: Executable path for STAR binary
    :param genomeDir: 
    :param limitRAM_option: maximum available RAM (bytes) for map reads process. Default: 40000000000
    :param num_threads:
    
    :type option: string
    :type reads: list
    :type folder: string 
    :type name: string 
    :type STAR_exe: string
    :type genomeDir: string 
    :type limitRAM_option: int
    :type num_threads: int
    
    
    """
    ## open file
    print("\t+ Mapping sample %s using STAR" %name)
    
    if not os.path.isdir(folder):
        folder = files_functions.create_folder(folder)
    ##
    bam_file_name = os.path.join(folder, 'Aligned.sortedByCoord.out.bam')
        
    ## read is a list with 1 or 2 read fastq files
    jread = " ".join(reads)

    ## prepare command
    cmd = "%s --genomeDir %s --runThreadN %s " %(STAR_exe, genomeDir, num_threads)
    cmd = cmd + "--limitBAMsortRAM %s --outFileNamePrefix %s " %(limitRAM_option, folder + '/')

    ## some common options
    cmd = cmd + "--alignSJDBoverhangMin 1000 --outFilterMultimapNmax 1 --outFilterMismatchNoverLmax 0.03 "
    cmd = cmd + "--outFilterScoreMinOverLread 0 --outFilterMatchNminOverLread 0 --outFilterMatchNmin 16 "
    cmd = cmd + "--alignIntronMax 1 --outSAMheaderHD @HD VN:1.4 SO:coordinate --outSAMtype BAM SortedByCoordinate "
    
    ## Multiple samples or just one?
    if option == 'LoadAndKeep':
        cmd = cmd + "--genomeLoad LoadAndKeep"
    else:
        cmd = cmd + "--genomeLoad NoSharedMemory"
    
    ## ReadFiles
    cmd = cmd + " --readFilesIn %s " %jread

    ## logfile & errfile
    logfile = os.path.join(folder, 'STAR.log')
    errfile = os.path.join(folder, 'STAR.err')
    cmd = cmd + ' > ' + logfile + ' 2> ' + errfile
    
    ## sent command
    mapping_code = system_call_functions.system_call(cmd, False, True)

    return (mapping_code)

###############

###########
def main():
    
    
    return 

######
if __name__== "__main__":
    main()
    
    
#######
# Usage: STAR  [options]... --genomeDir /path/to/genome/index/   --readFilesIn R1.fq R2.fq
# Spliced Transcripts Alignment to a Reference (c) Alexander Dobin, 2009-2019
########

#######
# For more details see:
# <https://github.com/alexdobin/STAR>
# <https://github.com/alexdobin/STAR/blob/master/doc/STARmanual.pdf>
# 
# ### versions
# versionGenome           2.7.1a
#     string: earliest genome index version compatible with this STAR release. Please do not change this value!
# 
# ### Parameter Files
# parametersFiles          -
#     string: name of a user-defined parameters file, "-": none. Can only be defined on the command line.
# 
# ### System
# sysShell            -
#     string: path to the shell binary, preferably bash, e.g. /bin/bash.
#                     - ... the default shell is executed, typically /bin/sh. This was reported to fail on some Ubuntu systems - then you need to specify path to bash.
# 
# ### Run Parameters
# runMode                         alignReads
#     string: type of the run.
# 
#                                 alignReads             ... map reads
#                                 genomeGenerate         ... generate genome files
#                                 inputAlignmentsFromBAM ... input alignments from BAM. Presently only works with --outWigType and --bamRemoveDuplicates.
#                                 liftOver               ... lift-over of GTF files (--sjdbGTFfile) between genome assemblies using chain file(s) from --genomeChainFiles.
# 
# runThreadN                      1
#     int: number of threads to run STAR
# 
# runDirPerm                      User_RWX
#     string: permissions for the directories created at the run-time.
#                                 User_RWX ... user-read/write/execute
#                                 All_RWX  ... all-read/write/execute (same as chmod 777)
# 
# runRNGseed                      777
#     int: random number generator seed.
# 
# 
# ### Genome Parameters
# genomeDir                   ./GenomeDir/
#     string: path to the directory where genome files are stored (for --runMode alignReads) or will be generated (for --runMode generateGenome)
# 
# genomeLoad                NoSharedMemory
#     string: mode of shared memory usage for the genome files. Only used with --runMode alignReads.
#                           LoadAndKeep     ... load genome into shared and keep it in memory after run
#                           LoadAndRemove   ... load genome into shared but remove it after run
#                           LoadAndExit     ... load genome into shared memory and exit, keeping the genome in memory for future runs
#                           Remove          ... do not map anything, just remove loaded genome from memory
#                           NoSharedMemory  ... do not use shared memory, each job will have its own private copy of the genome
# 
# genomeFastaFiles            -
#     string(s): path(s) to the fasta files with the genome sequences, separated by spaces. These files should be plain text FASTA files, they *cannot* be zipped.
#                             Required for the genome generation (--runMode genomeGenerate). Can also be used in the mapping (--runMode alignReads) to add extra (new) sequences to the genome (e.g. spike-ins).
# 
# genomeChainFiles            -
#     string: chain files for genomic liftover. Only used with --runMode liftOver .
# 
# genomeFileSizes             0
#     uint(s)>0: genome files exact sizes in bytes. Typically, this should not be defined by the user.
# 
# genomeConsensusFile         -
#     string: VCF file with consensus SNPs (i.e. alternative allele is the major (AF>0.5) allele)
# 
# ### Genome Indexing Parameters - only used with --runMode genomeGenerate
# genomeChrBinNbits           18
#     int: =log2(chrBin), where chrBin is the size of the bins for genome storage: each chromosome will occupy an integer number of bins. For a genome with large number of contigs, it is recommended to scale this parameter as min(18, log2[max(GenomeLength/NumberOfReferences,ReadLength)]).
# 
# genomeSAindexNbases         14
#     int: length (bases) of the SA pre-indexing string. Typically between 10 and 15. Longer strings will use much more memory, but allow faster searches. For small genomes, the parameter --genomeSAindexNbases must be scaled down to min(14, log2(GenomeLength)/2 - 1).
# 
# genomeSAsparseD             1
#     int>0: suffux array sparsity, i.e. distance between indices: use bigger numbers to decrease needed RAM at the cost of mapping speed reduction
# 
# genomeSuffixLengthMax       -1
#     int: maximum length of the suffixes, has to be longer than read length. -1 = infinite.
# 
# 
# ### Splice Junctions Database
# sjdbFileChrStartEnd                     -
#     string(s): path to the files with genomic coordinates (chr <tab> start <tab> end <tab> strand) for the splice junction introns. Multiple files can be supplied wand will be concatenated.
# 
# sjdbGTFfile                             -
#     string: path to the GTF file with annotations
# 
# sjdbGTFchrPrefix                        -
#     string: prefix for chromosome names in a GTF file (e.g. 'chr' for using ENSMEBL annotations with UCSC genomes)
# 
# sjdbGTFfeatureExon                      exon
#     string: feature type in GTF file to be used as exons for building transcripts
# 
# sjdbGTFtagExonParentTranscript          transcript_id
#     string: GTF attribute name for parent transcript ID (default "transcript_id" works for GTF files)
# 
# sjdbGTFtagExonParentGene                gene_id
#     string: GTF attribute name for parent gene ID (default "gene_id" works for GTF files)
# 
# sjdbGTFtagExonParentGeneName            gene_name
#     string(s): GTF attrbute name for parent gene name
# 
# sjdbGTFtagExonParentGeneType            gene_type gene_biotype
#     string(s): GTF attrbute name for parent gene type
# 
# sjdbOverhang                            100
#     int>0: length of the donor/acceptor sequence on each side of the junctions, ideally = (mate_length - 1)
# 
# sjdbScore                               2
#     int: extra alignment score for alignmets that cross database junctions
# 
# sjdbInsertSave                          Basic
#     string: which files to save when sjdb junctions are inserted on the fly at the mapping step
#                     Basic ... only small junction / transcript files
#                     All   ... all files including big Genome, SA and SAindex - this will create a complete genome directory
# 
# ### Variation parameters
# varVCFfile                              -
#     string: path to the VCF file that contains variation data.
# 
# ### Input Files
# inputBAMfile                -
#     string: path to BAM input file, to be used with --runMode inputAlignmentsFromBAM
# 
# ### Read Parameters
# readFilesType               Fastx
#     string: format of input read files
#                             Fastx       ... FASTA or FASTQ
#                             SAM SE      ... SAM or BAM single-end reads; for BAM use --readFilesCommand samtools view
#                             SAM PE      ... SAM or BAM paired-end reads; for BAM use --readFilesCommand samtools view
# 
# readFilesIn                 Read1 Read2
#     string(s): paths to files that contain input read1 (and, if needed,  read2)
# 
# readFilesPrefix             -
#     string: preifx for the read files names, i.e. it will be added in front of the strings in --readFilesIn
#                             -: no prefix
# 
# readFilesCommand             -
#     string(s): command line to execute for each of the input file. This command should generate FASTA or FASTQ text and send it to stdout
#                For example: zcat - to uncompress .gz files, bzcat - to uncompress .bz2 files, etc.
# 
# readMapNumber               -1
#     int: number of reads to map from the beginning of the file
#                             -1: map all reads
# 
# readMatesLengthsIn          NotEqual
#     string: Equal/NotEqual - lengths of names,sequences,qualities for both mates are the same  / not the same. NotEqual is safe in all situations.
# 
# readNameSeparator           /
#     string(s): character(s) separating the part of the read names that will be trimmed in output (read name after space is always trimmed)
# 
# readQualityScoreBase        33
#     int>=0: number to be subtracted from the ASCII code to get Phred quality score
# 
# clip3pNbases                 0
#     int(s): number(s) of bases to clip from 3p of each mate. If one value is given, it will be assumed the same for both mates.
# 
# clip5pNbases                 0
#     int(s): number(s) of bases to clip from 5p of each mate. If one value is given, it will be assumed the same for both mates.
# 
# clip3pAdapterSeq            -
#     string(s): adapter sequences to clip from 3p of each mate.  If one value is given, it will be assumed the same for both mates.
# 
# clip3pAdapterMMp            0.1
#     double(s): max proportion of mismatches for 3p adpater clipping for each mate.  If one value is given, it will be assumed the same for both mates.
# 
# clip3pAfterAdapterNbases    0
#     int(s): number of bases to clip from 3p of each mate after the adapter clipping. If one value is given, it will be assumed the same for both mates.
# 
# 
# ### Limits
# limitGenomeGenerateRAM               31000000000
#     int>0: maximum available RAM (bytes) for genome generation
# 
# limitIObufferSize                    150000000
#     int>0: max available buffers size (bytes) for input/output, per thread
# 
# limitOutSAMoneReadBytes              100000
#     int>0: max size of the SAM record (bytes) for one read. Recommended value: >(2*(LengthMate1+LengthMate2+100)*outFilterMultimapNmax
# 
# limitOutSJoneRead                    1000
#     int>0: max number of junctions for one read (including all multi-mappers)
# 
# limitOutSJcollapsed                  1000000
#     int>0: max number of collapsed junctions
# 
# limitBAMsortRAM                         0
#     int>=0: maximum available RAM (bytes) for sorting BAM. If =0, it will be set to the genome index size. 0 value can only be used with --genomeLoad NoSharedMemory option.
# 
# limitSjdbInsertNsj                     1000000
#     int>=0: maximum number of junction to be inserted to the genome on the fly at the mapping stage, including those from annotations and those detected in the 1st step of the 2-pass run
# 
# limitNreadsSoft                        -1
#     int: soft limit on the number of reads
# 
# ### Output: general
# outFileNamePrefix               ./
#     string: output files name prefix (including full or relative path). Can only be defined on the command line.
# 
# outTmpDir                       -
#     string: path to a directory that will be used as temporary by STAR. All contents of this directory will be removed!
#             - the temp directory will default to outFileNamePrefix_STARtmp
# 
# outTmpKeep                      None
#     string: whether to keep the tempporary files after STAR runs is finished
#                                 None ... remove all temporary files
#                                 All .. keep all files
# 
# outStd                          Log
#     string: which output will be directed to stdout (standard out)
#                                 Log                    ... log messages
#                                 SAM                    ... alignments in SAM format (which normally are output to Aligned.out.sam file), normal standard output will go into Log.std.out
#                                 BAM_Unsorted           ... alignments in BAM format, unsorted. Requires --outSAMtype BAM Unsorted
#                                 BAM_SortedByCoordinate ... alignments in BAM format, unsorted. Requires --outSAMtype BAM SortedByCoordinate
#                                 BAM_Quant              ... alignments to transcriptome in BAM format, unsorted. Requires --quantMode TranscriptomeSAM
# 
# outReadsUnmapped                None
#    string: output of unmapped and partially mapped (i.e. mapped only one mate of a paired end read) reads in separate file(s).
#                                 None    ... no output
#                                 Fastx   ... output in separate fasta/fastq files, Unmapped.out.mate1/2
# 
# outQSconversionAdd              0
#    int: add this number to the quality score (e.g. to convert from Illumina to Sanger, use -31)
# 
# outMultimapperOrder             Old_2.4
#     string: order of multimapping alignments in the output files
#                                 Old_2.4             ... quasi-random order used before 2.5.0
#                                 Random              ... random order of alignments for each multi-mapper. Read mates (pairs) are always adjacent, all alignment for each read stay together. This option will become default in the future releases.
# 
# ### Output: SAM and BAM
# outSAMtype                      SAM
#     strings: type of SAM/BAM output
#                                 1st word:
#                                 BAM  ... output BAM without sorting
#                                 SAM  ... output SAM without sorting
#                                 None ... no SAM/BAM output
#                                 2nd, 3rd:
#                                 Unsorted           ... standard unsorted
#                                 SortedByCoordinate ... sorted by coordinate. This option will allocate extra memory for sorting which can be specified by --limitBAMsortRAM.
# 
# outSAMmode                      Full
#     string: mode of SAM output
#                                 None ... no SAM output
#                                 Full ... full SAM output
#                                 NoQS ... full SAM but without quality scores
# 
# outSAMstrandField                               None
#     string: Cufflinks-like strand field flag
#                                 None        ... not used
#                                 intronMotif ... strand derived from the intron motif. Reads with inconsistent and/or non-canonical introns are filtered out.
# 
# outSAMattributes                Standard
#     string: a string of desired SAM attributes, in the order desired for the output SAM
#                                 NH HI AS nM NM MD jM jI XS MC ch ... any combination in any order
#                                 None        ... no attributes
#                                 Standard    ... NH HI AS nM
#                                 All         ... NH HI AS nM NM MD jM jI MC ch
#                                 vA          ... variant allele
#                                 vG          ... genomic coordiante of the variant overlapped by the read
#                                 vW          ... 0/1 - alignment does not pass / passes WASP filtering. Requires --waspOutputMode SAMtag
#                                 STARsolo:
#                                 CR CY UR UY ... sequences and quality scores of cell barcodes and UMIs for the solo* demultiplexing
#                                 CB UB       ... error-corrected cell barcodes and UMIs for solo* demultiplexing. Requires --outSAMtype BAM SortedByCoordinate.
#                                 sM          ... assessment of CB and UMI
#                                 sS          ... sequence of the entire barcode (CB,UMI,adapter...)
#                                 sQ          ... quality of the entire barcode
#                                 Unsupported/undocumented:
#                                 rB          ... alignment block read/genomic coordinates
#                                 vR          ... read coordinate of the variant
# 
# outSAMattrIHstart               1
#     int>=0:                     start value for the IH attribute. 0 may be required by some downstream software, such as Cufflinks or StringTie.
# 
# outSAMunmapped                  None
#     string(s): output of unmapped reads in the SAM format
#                                 1st word:
#                                 None   ... no output
#                                 Within ... output unmapped reads within the main SAM file (i.e. Aligned.out.sam)
#                                 2nd word:
#                                 KeepPairs ... record unmapped mate for each alignment, and, in case of unsorted output, keep it adjacent to its mapped mate. Only affects multi-mapping reads.
# 
# outSAMorder                     Paired
#     string: type of sorting for the SAM output
#                                 Paired: one mate after the other for all paired alignments
#                                 PairedKeepInputOrder: one mate after the other for all paired alignments, the order is kept the same as in the input FASTQ files
# 
# outSAMprimaryFlag        OneBestScore
#     string: which alignments are considered primary - all others will be marked with 0x100 bit in the FLAG
#                                 OneBestScore ... only one alignment with the best score is primary
#                                 AllBestScore ... all alignments with the best score are primary
# 
# outSAMreadID            Standard
#     string: read ID record type
#                                 Standard ... first word (until space) from the FASTx read ID line, removing /1,/2 from the end
#                                 Number   ... read number (index) in the FASTx file
# 
# outSAMmapqUnique        255
#     int: 0 to 255: the MAPQ value for unique mappers
# 
# outSAMflagOR           0
#     int: 0 to 65535: sam FLAG will be bitwise OR'd with this value, i.e. FLAG=FLAG | outSAMflagOR. This is applied after all flags have been set by STAR, and after outSAMflagAND. Can be used to set specific bits that are not set otherwise.
# 
# outSAMflagAND           65535
#     int: 0 to 65535: sam FLAG will be bitwise AND'd with this value, i.e. FLAG=FLAG & outSAMflagOR. This is applied after all flags have been set by STAR, but before outSAMflagOR. Can be used to unset specific bits that are not set otherwise.
# 
# outSAMattrRGline        -
#     string(s): SAM/BAM read group line. The first word contains the read group identifier and must start with "ID:", e.g. --outSAMattrRGline ID:xxx CN:yy "DS:z z z".
#             xxx will be added as RG tag to each output alignment. Any spaces in the tag values have to be double quoted.
#             Comma separated RG lines correspons to different (comma separated) input files in --readFilesIn. Commas have to be surrounded by spaces, e.g.
#             --outSAMattrRGline ID:xxx , ID:zzz "DS:z z" , ID:yyy DS:yyyy
# 
# outSAMheaderHD          -
#     strings: @HD (header) line of the SAM header
# 
# outSAMheaderPG          -
#     strings: extra @PG (software) line of the SAM header (in addition to STAR)
# 
# outSAMheaderCommentFile -
#     string: path to the file with @CO (comment) lines of the SAM header
# 
# outSAMfilter            None
#     string(s): filter the output into main SAM/BAM files
#                         KeepOnlyAddedReferences ... only keep the reads for which all alignments are to the extra reference sequences added with --genomeFastaFiles at the mapping stage.
#                         KeepAllAddedReferences ...  keep all alignments to the extra reference sequences added with --genomeFastaFiles at the mapping stage.
# 
# 
# outSAMmultNmax          -1
#     int: max number of multiple alignments for a read that will be output to the SAM/BAM files.
#                         -1 ... all alignments (up to --outFilterMultimapNmax) will be output
# 
# outSAMtlen              1
#     int: calculation method for the TLEN field in the SAM/BAM files
#                         1 ... leftmost base of the (+)strand mate to rightmost base of the (-)mate. (+)sign for the (+)strand mate
#                         2 ... leftmost base of any mate to rightmost base of any mate. (+)sign for the mate with the leftmost base. This is different from 1 for overlapping mates with protruding ends
# 
# outBAMcompression       1
#     int: -1 to 10  BAM compression level, -1=default compression (6?), 0=no compression, 10=maximum compression
# 
# outBAMsortingThreadN    0
#     int: >=0: number of threads for BAM sorting. 0 will default to min(6,--runThreadN).
# 
# outBAMsortingBinsN      50
#     int: >0:  number of genome bins fo coordinate-sorting
# 
# ### BAM processing
# bamRemoveDuplicatesType  -
#     string: mark duplicates in the BAM file, for now only works with (i) sorted BAM fed with inputBAMfile, and (ii) for paired-end alignments only
#                         -                       ... no duplicate removal/marking
#                         UniqueIdentical         ... mark all multimappers, and duplicate unique mappers. The coordinates, FLAG, CIGAR must be identical
#                         UniqueIdenticalNotMulti  ... mark duplicate unique mappers but not multimappers.
# 
# bamRemoveDuplicatesMate2basesN   0
#     int>0: number of bases from the 5' of mate 2 to use in collapsing (e.g. for RAMPAGE)
# 
# ### Output Wiggle
# outWigType          None
#     string(s): type of signal output, e.g. "bedGraph" OR "bedGraph read1_5p". Requires sorted BAM: --outSAMtype BAM SortedByCoordinate .
#                     1st word:
#                     None       ... no signal output
#                     bedGraph   ... bedGraph format
#                     wiggle     ... wiggle format
#                     2nd word:
#                     read1_5p   ... signal from only 5' of the 1st read, useful for CAGE/RAMPAGE etc
#                     read2      ... signal from only 2nd read
# 
# outWigStrand        Stranded
#     string: strandedness of wiggle/bedGraph output
#                     Stranded   ...  separate strands, str1 and str2
#                     Unstranded ...  collapsed strands
# 
# outWigReferencesPrefix    -
#     string: prefix matching reference names to include in the output wiggle file, e.g. "chr", default "-" - include all references
# 
# outWigNorm              RPM
#     string: type of normalization for the signal
#                         RPM    ... reads per million of mapped reads
#                         None   ... no normalization, "raw" counts
# 
# ### Output Filtering
# outFilterType                   Normal
#     string: type of filtering
#                                 Normal  ... standard filtering using only current alignment
#                                 BySJout ... keep only those reads that contain junctions that passed filtering into SJ.out.tab
# 
# outFilterMultimapScoreRange     1
#     int: the score range below the maximum score for multimapping alignments
# 
# outFilterMultimapNmax           10
#     int: maximum number of loci the read is allowed to map to. Alignments (all of them) will be output only if the read maps to no more loci than this value.
#          Otherwise no alignments will be output, and the read will be counted as "mapped to too many loci" in the Log.final.out .
# 
# outFilterMismatchNmax           10
#     int: alignment will be output only if it has no more mismatches than this value.
# 
# outFilterMismatchNoverLmax      0.3
#     real: alignment will be output only if its ratio of mismatches to *mapped* length is less than or equal to this value.
# 
# outFilterMismatchNoverReadLmax  1.0
#     real: alignment will be output only if its ratio of mismatches to *read* length is less than or equal to this value.
# 
# 
# outFilterScoreMin               0
#     int: alignment will be output only if its score is higher than or equal to this value.
# 
# outFilterScoreMinOverLread      0.66
#     real: same as outFilterScoreMin, but  normalized to read length (sum of mates' lengths for paired-end reads)
# 
# outFilterMatchNmin              0
#     int: alignment will be output only if the number of matched bases is higher than or equal to this value.
# 
# outFilterMatchNminOverLread     0.66
#     real: sam as outFilterMatchNmin, but normalized to the read length (sum of mates' lengths for paired-end reads).
# 
# outFilterIntronMotifs           None
#     string: filter alignment using their motifs
#                 None                           ... no filtering
#                 RemoveNoncanonical             ... filter out alignments that contain non-canonical junctions
#                 RemoveNoncanonicalUnannotated  ... filter out alignments that contain non-canonical unannotated junctions when using annotated splice junctions database. The annotated non-canonical junctions will be kept.
# 
# outFilterIntronStrands          RemoveInconsistentStrands
#     string: filter alignments
#                 RemoveInconsistentStrands      ... remove alignments that have junctions with inconsistent strands
#                 None                           ... no filtering
# 
# ### Output Filtering: Splice Junctions
# outSJfilterReads                All
#     string: which reads to consider for collapsed splice junctions output
#                 All: all reads, unique- and multi-mappers
#                 Unique: uniquely mapping reads only
# 
# outSJfilterOverhangMin          30  12  12  12
#     4 integers:    minimum overhang length for splice junctions on both sides for: (1) non-canonical motifs, (2) GT/AG and CT/AC motif, (3) GC/AG and CT/GC motif, (4) AT/AC and GT/AT motif. -1 means no output for that motif
#                                 does not apply to annotated junctions
# 
# outSJfilterCountUniqueMin       3   1   1   1
#     4 integers: minimum uniquely mapping read count per junction for: (1) non-canonical motifs, (2) GT/AG and CT/AC motif, (3) GC/AG and CT/GC motif, (4) AT/AC and GT/AT motif. -1 means no output for that motif
#                                 Junctions are output if one of outSJfilterCountUniqueMin OR outSJfilterCountTotalMin conditions are satisfied
#                                 does not apply to annotated junctions
# 
# outSJfilterCountTotalMin     3   1   1   1
#     4 integers: minimum total (multi-mapping+unique) read count per junction for: (1) non-canonical motifs, (2) GT/AG and CT/AC motif, (3) GC/AG and CT/GC motif, (4) AT/AC and GT/AT motif. -1 means no output for that motif
#                                 Junctions are output if one of outSJfilterCountUniqueMin OR outSJfilterCountTotalMin conditions are satisfied
#                                 does not apply to annotated junctions
# 
# outSJfilterDistToOtherSJmin     10  0   5   10
#     4 integers>=0: minimum allowed distance to other junctions' donor/acceptor
#                                 does not apply to annotated junctions
# 
# outSJfilterIntronMaxVsReadN        50000 100000 200000
#     N integers>=0: maximum gap allowed for junctions supported by 1,2,3,,,N reads
#                                 i.e. by default junctions supported by 1 read can have gaps <=50000b, by 2 reads: <=100000b, by 3 reads: <=200000. by >=4 reads any gap <=alignIntronMax
#                                 does not apply to annotated junctions
# 
# ### Scoring
# scoreGap                     0
#     int: splice junction penalty (independent on intron motif)
# 
# scoreGapNoncan               -8
#     int: non-canonical junction penalty (in addition to scoreGap)
# 
# scoreGapGCAG                 -4
#     GC/AG and CT/GC junction penalty (in addition to scoreGap)
# 
# scoreGapATAC                 -8
#     AT/AC  and GT/AT junction penalty  (in addition to scoreGap)
# 
# scoreGenomicLengthLog2scale   -0.25
#     extra score logarithmically scaled with genomic length of the alignment: scoreGenomicLengthLog2scale*log2(genomicLength)
# 
# scoreDelOpen                 -2
#     deletion open penalty
# 
# scoreDelBase                 -2
#     deletion extension penalty per base (in addition to scoreDelOpen)
# 
# scoreInsOpen                 -2
#     insertion open penalty
# 
# scoreInsBase                 -2
#     insertion extension penalty per base (in addition to scoreInsOpen)
# 
# scoreStitchSJshift           1
#     maximum score reduction while searching for SJ boundaries inthe stitching step
# 
# 
# ### Alignments and Seeding
# 
# seedSearchStartLmax             50
#     int>0: defines the search start point through the read - the read is split into pieces no longer than this value
# 
# seedSearchStartLmaxOverLread    1.0
#     real: seedSearchStartLmax normalized to read length (sum of mates' lengths for paired-end reads)
# 
# seedSearchLmax       0
#     int>=0: defines the maximum length of the seeds, if =0 max seed lengthis infinite
# 
# seedMultimapNmax      10000
#     int>0: only pieces that map fewer than this value are utilized in the stitching procedure
# 
# seedPerReadNmax       1000
#     int>0: max number of seeds per read
# 
# seedPerWindowNmax     50
#     int>0: max number of seeds per window
# 
# seedNoneLociPerWindow    10
#     int>0: max number of one seed loci per window
# 
# seedSplitMin                12
#     int>0: min length of the seed sequences split by Ns or mate gap
# 
# alignIntronMin              21
#     minimum intron size: genomic gap is considered intron if its length>=alignIntronMin, otherwise it is considered Deletion
# 
# alignIntronMax              0
#     maximum intron size, if 0, max intron size will be determined by (2^winBinNbits)*winAnchorDistNbins
# 
# alignMatesGapMax            0
#     maximum gap between two mates, if 0, max intron gap will be determined by (2^winBinNbits)*winAnchorDistNbins
# 
# alignSJoverhangMin          5
#     int>0: minimum overhang (i.e. block size) for spliced alignments
# 
# alignSJstitchMismatchNmax   0 -1 0 0
#     4*int>=0: maximum number of mismatches for stitching of the splice junctions (-1: no limit).
#                             (1) non-canonical motifs, (2) GT/AG and CT/AC motif, (3) GC/AG and CT/GC motif, (4) AT/AC and GT/AT motif.
# 
# alignSJDBoverhangMin        3
#     int>0: minimum overhang (i.e. block size) for annotated (sjdb) spliced alignments
# 
# alignSplicedMateMapLmin     0
#     int>0: minimum mapped length for a read mate that is spliced
# 
# alignSplicedMateMapLminOverLmate 0.66
#     real>0: alignSplicedMateMapLmin normalized to mate length
# 
# alignWindowsPerReadNmax     10000
#     int>0: max number of windows per read
# 
# alignTranscriptsPerWindowNmax       100
#     int>0: max number of transcripts per window
# 
# alignTranscriptsPerReadNmax               10000
#     int>0: max number of different alignments per read to consider
# 
# alignEndsType           Local
#     string: type of read ends alignment
#                         Local             ... standard local alignment with soft-clipping allowed
#                         EndToEnd          ... force end-to-end read alignment, do not soft-clip
#                         Extend5pOfRead1   ... fully extend only the 5p of the read1, all other ends: local alignment
#                         Extend5pOfReads12 ... fully extend only the 5p of the both read1 and read2, all other ends: local alignment
# 
# alignEndsProtrude       0    ConcordantPair
#     int, string:        allow protrusion of alignment ends, i.e. start (end) of the +strand mate downstream of the start (end) of the -strand mate
#                         1st word: int: maximum number of protrusion bases allowed
#                         2nd word: string:
#                                             ConcordantPair ... report alignments with non-zero protrusion as concordant pairs
#                                             DiscordantPair ... report alignments with non-zero protrusion as discordant pairs
# 
# alignSoftClipAtReferenceEnds    Yes
#     string: allow the soft-clipping of the alignments past the end of the chromosomes
#                                 Yes ... allow
#                                 No  ... prohibit, useful for compatibility with Cufflinks
# 
# alignInsertionFlush     None
#     string: how to flush ambiguous insertion positions
#                         None    ... insertions are not flushed
#                         Right   ... insertions are flushed to the right
# 
# ### Paired-End reads
# peOverlapNbasesMin          0
#     int>=0:             minimum number of overlap bases to trigger mates merging and realignment
# 
# peOverlapMMp                0.01
#     real, >=0 & <1:     maximum proportion of mismatched bases in the overlap area
# 
# ### Windows, Anchors, Binning
# 
# winAnchorMultimapNmax           50
#     int>0: max number of loci anchors are allowed to map to
# 
# winBinNbits                     16
#     int>0: =log2(winBin), where winBin is the size of the bin for the windows/clustering, each window will occupy an integer number of bins.
# 
# winAnchorDistNbins              9
#     int>0: max number of bins between two anchors that allows aggregation of anchors into one window
# 
# winFlankNbins                   4
#     int>0: log2(winFlank), where win Flank is the size of the left and right flanking regions for each window
# 
# winReadCoverageRelativeMin      0.5
#     real>=0: minimum relative coverage of the read sequence by the seeds in a window, for STARlong algorithm only.
# 
# winReadCoverageBasesMin      0
#     int>0: minimum number of bases covered by the seeds in a window , for STARlong algorithm only.
# 
# ### Chimeric Alignments
# chimOutType                 Junctions
#     string(s): type of chimeric output
#                             Junctions       ... Chimeric.out.junction
#                             SeparateSAMold  ... output old SAM into separate Chimeric.out.sam file
#                             WithinBAM       ... output into main aligned BAM files (Aligned.*.bam)
#                             WithinBAM HardClip  ... (default) hard-clipping in the CIGAR for supplemental chimeric alignments (defaultif no 2nd word is present)
#                             WithinBAM SoftClip  ... soft-clipping in the CIGAR for supplemental chimeric alignments
# 
# chimSegmentMin              0
#     int>=0: minimum length of chimeric segment length, if ==0, no chimeric output
# 
# chimScoreMin                0
#     int>=0: minimum total (summed) score of the chimeric segments
# 
# chimScoreDropMax            20
#     int>=0: max drop (difference) of chimeric score (the sum of scores of all chimeric segments) from the read length
# 
# chimScoreSeparation         10
#     int>=0: minimum difference (separation) between the best chimeric score and the next one
# 
# chimScoreJunctionNonGTAG    -1
#     int: penalty for a non-GT/AG chimeric junction
# 
# chimJunctionOverhangMin     20
#     int>=0: minimum overhang for a chimeric junction
# 
# chimSegmentReadGapMax       0
#     int>=0: maximum gap in the read sequence between chimeric segments
# 
# chimFilter                  banGenomicN
#     string(s): different filters for chimeric alignments
#                             None ... no filtering
#                             banGenomicN ... Ns are not allowed in the genome sequence around the chimeric junction
# 
# chimMainSegmentMultNmax        10
#     int>=1: maximum number of multi-alignments for the main chimeric segment. =1 will prohibit multimapping main segments.
# 
# chimMultimapNmax                    0
#     int>=0: maximum number of chimeric multi-alignments
#                                 0 ... use the old scheme for chimeric detection which only considered unique alignments
# 
# chimMultimapScoreRange          1
#     int>=0: the score range for multi-mapping chimeras below the best chimeric score. Only works with --chimMultimapNmax > 1
# 
# chimNonchimScoreDropMin         20
#     int>=0: to trigger chimeric detection, the drop in the best non-chimeric alignment score with respect to the read length has to be greater than this value
# 
# chimOutJunctionFormat           0
#     int: formatting type for the Chimeric.out.junction file
#                                 0 ... no comment lines/headers
#                                 1 ... comment lines at the end of the file: command line and Nreads: total, unique, multi
# 
# ### Quantification of Annotations
# quantMode                   -
#     string(s): types of quantification requested
#                             -                ... none
#                             TranscriptomeSAM ... output SAM/BAM alignments to transcriptome into a separate file
#                             GeneCounts       ... count reads per gene
# 
# quantTranscriptomeBAMcompression    1       1
#     int: -2 to 10  transcriptome BAM compression level
#                             -2  ... no BAM output
#                             -1  ... default compression (6?)
#                              0  ... no compression
#                              10 ... maximum compression
# 
# quantTranscriptomeBan       IndelSoftclipSingleend
#     string: prohibit various alignment type
#                             IndelSoftclipSingleend  ... prohibit indels, soft clipping and single-end alignments - compatible with RSEM
#                             Singleend               ... prohibit single-end alignments
# 
# ### 2-pass Mapping
# twopassMode                 None
#     string: 2-pass mapping mode.
#                             None        ... 1-pass mapping
#                             Basic       ... basic 2-pass mapping, with all 1st pass junctions inserted into the genome indices on the fly
# 
# twopass1readsN              -1
#     int: number of reads to process for the 1st step. Use very large number (or default -1) to map all reads in the first step.
# 
# 
# ### WASP parameters
# waspOutputMode              None
#     string: WASP allele-specific output type. This is re-implemenation of the original WASP mappability filtering by Bryce van de Geijn, Graham McVicker, Yoav Gilad & Jonathan K Pritchard. Please cite the original WASP paper: Nature Methods 12, 1061–1063 (2015), https://www.nature.com/articles/nmeth.3582 .
#                             SAMtag      ... add WASP tags to the alignments that pass WASP filtering
# 
# ### STARsolo (single cell RNA-seq) parameters
# soloType                    None
#     string(s): type of single-cell RNA-seq
#                             CB_UMI_Simple   ... (a.k.a. Droplet) one UMI and one Cell Barcode of fixed length in read2, e.g. Drop-seq and 10X Chromium
#                             CB_UMI_Complex  ... one UMI of fixed length, but multiple Cell Barcodes of varying length, as well as adapters sequences are allowed in read2 only, e.g. inDrop.
# 
# soloCBwhitelist             -
#     string(s): file(s) with whitelist(s) of cell barcodes. Only one file allowed with 
# 
# soloCBstart                 1
#     int>0: cell barcode start base
# 
# soloCBlen                   16
#     int>0: cell barcode length
# 
# soloUMIstart                17
#     int>0: UMI start base
# 
# soloUMIlen                  10
#     int>0: UMI length
# 
# soloBarcodeReadLength       1
#     int: length of the barcode read
#                             1   ... equal to sum of soloCBlen+soloUMIlen
#                             0   ... not defined, do not check
# 
# soloCBposition              -
#     strings(s)              position of Cell Barcode(s) on the barcode read.
#                             Presently only works with --soloType CB_UMI_Complex, and barcodes are assumed to be on Read2.
#                             Format for each barcode: startAnchor_startDistance_endAnchor_endDistance
#                             start(end)Anchor defines the anchor base for the CB: 0: read start; 1: read end; 2: adapter start; 3: adapter end
#                             start(end)Distance is the distance from the CB start(end) to the Anchor base
#                             String for different barcodes are separated by space.
#                             Example: inDrop (Zilionis et al, Nat. Protocols, 2017):
#                             --soloCBposition  0_0_2_-1  3_1_3_8
# 
# soloUMIposition             -
#     string                  position of the UMI on the barcode read, same as soloCBposition
#                             Example: inDrop (Zilionis et al, Nat. Protocols, 2017):
#                             --soloCBposition  3_9_3_14
# 
# soloAdapterSequence         -
#     string:                 adapter sequence to anchor barcodes.
# 
# soloAdapterMismatchesNmax   1
#     int>0:                  maximum number of mismatches allowed in adapter sequence.
# 
# soloCBmatchWLtype           1MM_multi
#     string:                 matching the Cell Barcodes to the WhiteList
#                             Exact                   ... only exact matches allowed
#                             1MM                     ... only one match in whitelist with 1 mismatched base allowed. Allowed CBs have to have at least one read with exact match.
#                             1MM_multi               ... multiple matches in whitelist with 1 mismatched base allowed, posterior probability calculation is used choose one of the matches. 
#                                                         Allowed CBs have to have at least one read with exact match. Similar to CellRanger 2.2.0
#                             1MM_multi_pseudocounts  ... same as 1MM_Multi, but pseudocounts of 1 are added to all whitelist barcodes.
#                                                         Similar to CellRanger 3.x.x
# 
# soloStrand                  Forward
#     string: strandedness of the solo libraries:
#                             Unstranded  ... no strand information
#                             Forward     ... read strand same as the original RNA molecule
#                             Reverse     ... read strand opposite to the original RNA molecule
# 
# soloFeatures                Gene
#     string(s):              genomic features for which the UMI counts per Cell Barcode are collected
#                             Gene            ... genes: reads match the gene transcript
#                             SJ              ... splice junctions: reported in SJ.out.tab
#                             GeneFull        ... full genes: count all reads overlapping genes' exons and introns
#                             Transcript3p   ... quantification of transcript for 3' protocols
# 
# soloUMIdedup                1MM_All
#     string(s):              type of UMI deduplication (collapsing) algorithm
#                             1MM_All             ... all UMIs with 1 mismatch distance to each other are collapsed (i.e. counted once)
#                             1MM_Directional     ... follows the "directional" method from the UMI-tools by Smith, Heger and Sudbery (Genome Research 2017).
#                             Exact               ... only exactly matching UMIs are collapsed
# 
# soloUMIfiltering            -
#     string(s)               type of UMI filtering
#                             -               ... basic filtering: remove UMIs with N and homopolymers (similar to CellRanger 2.2.0)
#                             MultiGeneUMI    ... remove lower-count UMIs that map to more than one gene (introduced in CellRanger 3.x.x)
# 
# soloOutFileNames            Solo.out/          features.tsv barcodes.tsv        matrix.mtx
#     string(s)               file names for STARsolo output:
#                             file_name_prefix   gene_names   barcode_sequences   cell_feature_count_matrix
# 
# soloCellFilter              CellRanger2.2 3000 0.99 10
#     string(s):              cell filtering type and parameters
#                             CellRanger2.2   ... simple filtering of CellRanger 2.2, followed by thre numbers: number of expected cells, robust maximum percentile for UMI count, maximum to minimum ratio for UMI count
#                             TopCells        ... only report top cells by UMI count, followed by the excat number of cells
#                             None            ... do not output filtered cells
# 
#######
