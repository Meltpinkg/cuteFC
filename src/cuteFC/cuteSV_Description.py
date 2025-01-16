''' 
 * All rights Reserved, Designed By HIT-Bioinformatics   
 * @Title:  cuteSV_Description.py
 * @author: tjiang & sqcao & zdzhang
 * @date: Jan. 16th 2025
 * @version V1.0.1
'''
import argparse

VERSION = '1.0.1'

class cuteFCdp(object):
	'''
	Detailed descriptions of cuteFC version and its parameters.
	'''

	USAGE="""\
		
	Current version: v%s
	Author: Tao Jiang
	Contact: tjiang@hit.edu.cn

	Suggestions:

	For PacBio CLR data:
		--max_cluster_bias_INS		500
		--diff_ratio_merging_INS	0.5
		--max_cluster_bias_DEL	1000
		--diff_ratio_merging_DEL	0.5

	For PacBio CCS(HIFI) data:
		--max_cluster_bias_INS		1000
		--diff_ratio_merging_INS	0.9
		--max_cluster_bias_DEL	1000
		--diff_ratio_merging_DEL	0.5

	For ONT data:
		--max_cluster_bias_INS		1000
		--diff_ratio_merging_INS	0.5
		--max_cluster_bias_DEL	1000
		--diff_ratio_merging_DEL	0.5


	"""%(VERSION)


def parseArgs(argv):
	parser = argparse.ArgumentParser(prog="cuteFC", 
		description=cuteFCdp.USAGE, 
		formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument('--version', '-v', 
		action = 'version', 
		version = '%(prog)s {version}'.format(version=VERSION))

	# **************Parameters of input******************
	parser.add_argument("input", 
		metavar="[BAM]", 
		type = str, 
		help ="Sorted .bam file from NGMLR or Minimap2.")
	parser.add_argument("reference",  
		type = str, 
		help ="The reference genome in fasta format.")
	parser.add_argument('output', 
		type = str, 
		help = "Output VCF format file.")
	parser.add_argument('work_dir', 
		type = str, 
		help = "Work-directory for distributed jobs")

	# **************Parameters in force calling******************
	GroupGenotype = parser.add_argument_group('Force calling')
	GroupGenotype.add_argument('-Ivcf', #'--MERGED_VCF',
		help = "Given essential vcf file of target SVs. Enable to perform force calling. [NULL]",
		default = None,
        type = str,
		required=True)

	# ************** Other Parameters******************
	parser.add_argument('-t', '--threads', 
		help = "Number of threads to use.[%(default)s]", 
		default = 16, 
		type = int)
	parser.add_argument('-b', '--batches', 
		help = "Batch of genome segmentation interval.[%(default)s]", 
		default = 10000000, 
		type = int)
	# The description of batches needs to improve.
	parser.add_argument('-S', '--sample',
		help = "Sample name/id",
		default = "NULL",
		type = str)

	parser.add_argument('--retain_work_dir',
		help = "Enable to retain temporary folder and files.",
		action="store_true")
	
	parser.add_argument('--write_old_sigs',
		help = "Enable to write sigs file in temporary folder for legacy compatibilities.",
		action="store_true")

	parser.add_argument('--report_readid',
		help = "Enable to report supporting read ids for each SV.",
		action="store_true")

	# **************Parameters in signatures collection******************
	GroupSignaturesCollect = parser.add_argument_group('Collection of SV signatures')
	GroupSignaturesCollect.add_argument('-p', '--max_split_parts', 
		help = "Maximum number of split segments a read may be aligned before it is ignored. All split segments are considered when using -1. \
			(Recommand -1 when applying assembly-based alignment.)[%(default)s]", 
		default = 7, 
		type = int)
	GroupSignaturesCollect.add_argument('-q', '--min_mapq', 
		help = "Minimum mapping quality value of alignment to be taken into account.[%(default)s]", 
		default = 10, 
		type = int)
	GroupSignaturesCollect.add_argument('-r', '--min_read_len', 
		help = "Ignores reads that only report alignments with not longer than bp.[%(default)s]", 
		default = 500, 
		type = int)
	GroupSignaturesCollect.add_argument('-md', '--merge_del_threshold', 
		help = "Maximum distance of deletion signals to be merged. In our paper, I used -md 500 to process HG002 real human sample data.[%(default)s]", 
		default = 0, 
		type = int)
	GroupSignaturesCollect.add_argument('-mi', '--merge_ins_threshold', 
		help = "Maximum distance of insertion signals to be merged. In our paper, I used -mi 500 to process HG002 real human sample data.[%(default)s]", 
		default = 100, 
		type = int)
	GroupSignaturesCollect.add_argument('-include_bed', 
		help = "Optional given bed file. Only detect SVs in regions in the BED file. [NULL]",
		default = None,
        type = str)

	# **************Parameters in clustering******************
	GroupSVCluster = parser.add_argument_group('Generation of SV clusters')
	GroupSVCluster.add_argument('-s', '--min_support', 
		help = "Minimum number of reads that support a SV to be reported.[%(default)s]", 
		default = 10, 
		type = int)
	GroupSVCluster.add_argument('-l', '--min_size', 
		help = "Minimum size of SV to be reported.[%(default)s]", 
		default = 30, 
		type = int)
	GroupSVCluster.add_argument('-L', '--max_size', 
		help = "Maximum size of SV to be reported. All SVs are reported when using -1. [%(default)s]", 
		default = 100000, 
		type = int)
	GroupSVCluster.add_argument('-sl', '--min_siglength', 
		help = "Minimum length of SV signal to be extracted.[%(default)s]", 
		default = 10, 
		type = int)

	# **************Parameters in genotyping******************
	GroupGenotype.add_argument('--genotype',
		help = "Enable to generate genotypes.",
		action="store_true")
	GroupGenotype.add_argument('--gt_round', 
		help = "Maximum round of iteration for alignments searching if perform genotyping.[%(default)s]", 
		default = 500, 
		type = int)
	GroupGenotype.add_argument('--read_range', 
		help = "The interval range for counting reads distribution.[%(default)s]", 
		default = 1000, 
		type = int)
	GroupGenotype.add_argument('--detect_large_ins', 
		help = "Enable the detection of large insertions.",
		action="store_true")

	# **************Advanced Parameters******************
	GroupAdvanced = parser.add_argument_group('Advanced')

	# ++++++INS++++++
	GroupAdvanced.add_argument('--max_cluster_bias_INS', 
		help = "Maximum distance to cluster read together for insertion.[%(default)s]", 
		default = 100, 
		type = int)
	GroupAdvanced.add_argument('--diff_ratio_merging_INS', 
		help = "Do not merge breakpoints with basepair identity more than [%(default)s] for insertion.", 
		default = 0.3, 
		type = float)
	# GroupAdvanced.add_argument('--diff_ratio_filtering_INS', 
	# 	help = "Filter breakpoints with basepair identity less than [%(default)s] for insertion.", 
	# 	default = 0.6, 
	# 	type = float)

	# ++++++DEL++++++
	GroupAdvanced.add_argument('--max_cluster_bias_DEL', 
		help = "Maximum distance to cluster read together for deletion.[%(default)s]", 
		default = 200, 
		type = int)
	GroupAdvanced.add_argument('--diff_ratio_merging_DEL', 
		help = "Do not merge breakpoints with basepair identity more than [%(default)s] for deletion.", 
		default = 0.5, 
		type = float)
	# GroupAdvanced.add_argument('--diff_ratio_filtering_DEL', 
	# 	help = "Filter breakpoints with basepair identity less than [%(default)s] for deletion.", 
	# 	default = 0.7, 
	# 	type = float)

	# ++++++INV++++++
	GroupAdvanced.add_argument('--max_cluster_bias_INV', 
		help = "Maximum distance to cluster read together for inversion.[%(default)s]", 
		default = 500, 
		type = int)

	# ++++++DUP++++++
	GroupAdvanced.add_argument('--max_cluster_bias_DUP', 
		help = "Maximum distance to cluster read together for duplication.[%(default)s]", 
		default = 500, 
		type = int)

	# ++++++TRA++++++
	GroupAdvanced.add_argument('--max_cluster_bias_TRA', 
		help = "Maximum distance to cluster read together for translocation.[%(default)s]", 
		default = 50, 
		type = int)
	GroupAdvanced.add_argument('--diff_ratio_filtering_TRA', 
		help = "Filter breakpoints with basepair identity less than [%(default)s] for translocation.", 
		default = 0.6, 
		type = float)

	GroupAdvanced.add_argument('--remain_reads_ratio', 
		help = "The ratio of reads remained in cluster. Set lower when the alignment data have high quality but recommand over 0.5.[%(default)s]", 
		default = 1.0, 
		type = float)

	args = parser.parse_args(argv)
	return args

def Generation_VCF_header(file, contiginfo, sample, argv):
	# General header
	file.write("##fileformat=VCFv4.2\n")
	file.write("##source=cuteFC-%s\n"%(VERSION))
	import time
	file.write("##fileDate=%s\n"%(time.strftime('%Y-%m-%d %H:%M:%S %w-%Z',time.localtime())))
	for i in contiginfo:
		file.write("##contig=<ID=%s,length=%d>\n"%(i[0], i[1]))

	# Specific header
	# ALT
	file.write("##ALT=<ID=INS,Description=\"Insertion of novel sequence relative to the reference\">\n")
	file.write("##ALT=<ID=DEL,Description=\"Deletion relative to the reference\">\n")
	file.write("##ALT=<ID=DUP,Description=\"Region of elevated copy number relative to the reference\">\n")
	file.write("##ALT=<ID=INV,Description=\"Inversion of reference sequence\">\n")
	file.write("##ALT=<ID=BND,Description=\"Breakend of translocation\">\n")

	# INFO
	file.write("##INFO=<ID=PRECISE,Number=0,Type=Flag,Description=\"Precise structural variant\">\n")
	file.write("##INFO=<ID=IMPRECISE,Number=0,Type=Flag,Description=\"Imprecise structural variant\">\n")
	file.write("##INFO=<ID=SVTYPE,Number=1,Type=String,Description=\"Type of structural variant\">\n")
	file.write("##INFO=<ID=SVLEN,Number=1,Type=Integer,Description=\"Difference in length between REF and ALT alleles\">\n")
	file.write("##INFO=<ID=CHR2,Number=1,Type=String,Description=\"Chromosome for END coordinate in case of a translocation\">\n")
	file.write("##INFO=<ID=END,Number=1,Type=Integer,Description=\"End position of the variant described in this record\">\n")
	file.write("##INFO=<ID=CIPOS,Number=2,Type=Integer,Description=\"Confidence interval around POS for imprecise variants\">\n")
	file.write("##INFO=<ID=CILEN,Number=2,Type=Integer,Description=\"Confidence interval around inserted/deleted material between breakends\">\n")
	# file.write("##INFO=<ID=MATEID,Number=.,Type=String,Description=\"ID of mate breakends\">\n")
	file.write("##INFO=<ID=RE,Number=1,Type=Integer,Description=\"Number of read support this record\">\n")
	file.write("##INFO=<ID=STRAND,Number=A,Type=String,Description=\"Strand orientation of the adjacency in BEDPE format (DEL:+-, DUP:-+, INV:++/--)\">\n")
	file.write("##INFO=<ID=RNAMES,Number=.,Type=String,Description=\"Supporting read names of SVs (comma separated)\">\n")
	file.write("##INFO=<ID=AF,Number=A,Type=Float,Description=\"Allele Frequency.\">\n")
	file.write("##FILTER=<ID=q5,Description=\"Quality below 5\">\n")
	# FORMAT
	# file.write("\n")
	file.write("##FORMAT=<ID=GT,Number=1,Type=String,Description=\"Genotype\">\n")
	file.write("##FORMAT=<ID=DR,Number=1,Type=Integer,Description=\"# High-quality reference reads\">\n")
	file.write("##FORMAT=<ID=DV,Number=1,Type=Integer,Description=\"# High-quality variant reads\">\n")
	file.write("##FORMAT=<ID=PL,Number=G,Type=Integer,Description=\"# Phred-scaled genotype likelihoods rounded to the closest integer\">\n")
	file.write("##FORMAT=<ID=GQ,Number=1,Type=Integer,Description=\"# Genotype quality\">\n")

	file.write("##CommandLine=\"cuteFC %s\"\n"%(" ".join(argv)))
