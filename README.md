# cuteFC

---
### Getting Start
	                                               __________    ___________      
	                                              |   ____   |  |   _____  |   
	                          _                   |  |    |__|  | /      | |
	 _______    _     _   ___| |___     ______    |  |          | |      |_|   
	|  ___  |  | |   | | |___   ___|   / ____ \   |  |_______   | |    
	| |   |_|  | |   | |     | |      / /____\ \  |   _______|  | | 
	| |        | |   | |     | |      | _______|  |  |          | |       _
	| |    _   | |   | |     | |  _   | |     _   |  |          | |      | |
	| |___| |  | |___| |     | |_| |  \ \____/ |  |  |          | \______| |
	|_______|  |_______|     |_____|   \______/   |__|          |__________|


---	
### Installation

	$ git clone https://github.com/tjiangHIT/cuteFC.git && cd cuteFC/ && python setup.py install 

---	
### Introduction
Accurate genotype assignment for SVs remains challenging, especially in large-scale joint calling. We develop cuteFC to achieve accurate and efficient regenotyping of SVs through a force-calling approach. Benchmarking results demonstrated that cuteFC outperforms state-of-the-art methods with 2%~5% higher F1 scores. SV joint-calling within the cohort revealed that cuteFC constructs the higher-quality genomic atlas with minimal computational resources. These results prove cuteFC to be a scalable and robust approach suitable for clinical applications, population studies, and related fields. 

For more detailed implementation of SV benchmarks, we show an example [here](https://github.com/tjiangHIT/cuteFC/tree/master/src/documentation).

BTW, the whole functions in cuteFC have been integrated into our previous SV detector, [cuteSV](https://github.com/tjiangHIT/cuteSV)

---
### Dependence
	
	1. python3
	2. pysam
	3. Biopython
	4. cigar
	5. numpy
	6. pyvcf

---
### Usage
	cuteFC <sorted.bam> <reference.fa> <output.vcf> <work_dir> -Ivcf <target.vcf>
	
*Suggestions*

	> For PacBio CLR data:
		--max_cluster_bias_INS		500
		--diff_ratio_merging_INS	0.5
		--max_cluster_bias_DEL	1000
		--diff_ratio_merging_DEL	0.5

	> For PacBio CCS(HIFI) data:
		--max_cluster_bias_INS		1000
		--diff_ratio_merging_INS	0.9
		--max_cluster_bias_DEL	1000
		--diff_ratio_merging_DEL	0.5

	> For ONT data:
		--max_cluster_bias_INS		1000
		--diff_ratio_merging_INS	0.5
		--max_cluster_bias_DEL	1000
		--diff_ratio_merging_DEL	0.5
	
| Parameter | Description | Default |
| :------------ |:---------------|-------------:|
|--threads|Number of threads to use.| 16 |
|--batches| Batch of genome segmentation interval.|10,000,000|
|--sample| Sample name/id |NULL|
|--retain_work_dir|Enable to retain temporary folder and files.|False|
|--write_old_sigs|Enable to output temporary sig files.|False|
|--report_readid|Enable to report supporting read ids for each SV.|False|
|--max_split_parts|Maximum number of split segments a read may be aligned before it is ignored. All split segments are considered when using -1. (Recommand -1 when applying assembly-based alignment.)|7|
|--min_mapq|Minimum mapping quality value of alignment to be taken into account.|10|
|--min_read_len|Ignores reads that only report alignments with not longer than bp.|500|
|--merge_del_threshold|Maximum distance of deletion signals to be merged.|0|
|--merge_ins_threshold|Maximum distance of insertion signals to be merged.|100|
|--min_support|Minimum number of reads that support a SV to be reported.|10|
|--min_size|Minimum length of SV to be reported.|30|
|--max_size|Maximum size of SV to be reported. Full length SVs are reported when using -1.|100000|
|--genotype|Enable to generate genotypes.|False|
|--gt_round|Maximum round of iteration for alignments searching if perform genotyping.|500|
|--read_range|The interval range for counting reads distribution.|1000|
|-Ivcf|Optional given vcf file. Enable to perform force calling.|NULL|
|--max_cluster_bias_INS|Maximum distance to cluster read together for insertion.|100|
|--diff_ratio_merging_INS|Do not merge breakpoints with basepair identity more than the ratio of *default* for insertion.|0.3|
|--max_cluster_bias_DEL|Maximum distance to cluster read together for deletion.|200|
|--diff_ratio_merging_DEL|Do not merge breakpoints with basepair identity more than the ratio of *default* for deletion.|0.5|
|--max_cluster_bias_INV|Maximum distance to cluster read together for inversion.|500|
|--max_cluster_bias_DUP|Maximum distance to cluster read together for duplication.|500|
|--max_cluster_bias_TRA|Maximum distance to cluster read together for translocation.|50|
|--diff_ratio_filtering_TRA|Filter breakpoints with basepair identity less than the ratio of *default* for translocation.|0.6|
|--remain_reads_ratio|The ratio of reads remained in cluster to generate the breakpoint. Set lower to get more precise breakpoint when the alignment data have high quality but recommand over 0.5.|1|
|-include_bed|Optional given bed file. Only detect SVs in regions in the BED file.|NULL|



---
### Citation
Cao S et al. Re-genotyping structural variants through an accurate force-calling method. bioRxiv 2022.08.29.505534; doi: https://doi.org/10.1101/2022.08.29.505534
	
---
### Contact
For advising, bug reporting, and requiring help, please post on [Github Issue](https://github.com/Meltpinkg/cuteFC/issues) or contact tjiang@hit.edu.cn.
