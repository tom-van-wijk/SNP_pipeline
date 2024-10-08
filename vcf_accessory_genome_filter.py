#!/usr/bin/env python

# Name:         vcf_accessory_genome_filter.py
# Author:       Tom van Wijk
# Date:         16-06-2018
# Licence:      GNU General Public License v3.0, copy provided in repository

# Reads a .vcf file and reference file and filteres out ass accessory genome
# snp locations, writes output to new .vcf files.
# This script is part of the SNP_pipeline.

# For detailed information and instruction on how to install and use this software
# please vieuw the included "README.md" file in this repository

# import python libraries
from argparse import ArgumentParser
import sys
import os


# Function to parse the command-line arguments
# Returns a namespace with argument keys and values
def parse_arguments(args):
	parser = ArgumentParser(prog="vcf_samplename_editor.py")
	parser.add_argument("-i", "--infile", dest = "input_file",
		action = "store", default = None, type = str,
		help = "Location of input .vsf file (required)",
		required = True)
	parser.add_argument("-r" "--reference", dest = "reference",
		action = "store", default = "NC_011205", type = str,
		help = "Reference genome (default=NC_011205)")
	return parser.parse_args()


# MAIN function
def main():
	# parse command line arguments
	args = parse_arguments(sys.argv)
	# read .samplefile and make dictionary of lines
	gene_positions = []
	with open(os.environ['SNP_REF']+"/"+args.reference+"_genes.csv", "r") as csv_file: 
		header = True
		for line in csv_file:
			if header == False:
				start = line.split(';"')[4].replace('"', '')
				end = int(line.split(';"')[4].replace('"', ''))+int(line.split(';"')[5].replace('"', ''))
				#print "START\t"+str(start)
				#print "END\t"+str(end)
				gene_positions.append(start+"-"+str(end))
			header = False
	csv_file.close()
	with open(args.input_file, "r") as infile, open(args.input_file.replace(".vcf", "_no_accessory.vcf"), "w") as outfile:
		write_to_out = "header"
		#genes = 0
		#accessory = 0
		for line in infile:
			if write_to_out == "header":
				outfile.write(line)
			elif write_to_out == "body":
				pos = False
				for gene in gene_positions:
					start = int(gene.split("-")[0])
					end = int(gene.split("-")[1])
					if start <= int(line.split("\t")[1]) <= end:
						pos =  True
				if pos ==  True:
					outfile.write(line)
					#genes += 1
				#else:
				#	accessory += 1
				#print "GENES:\t"+str(genes)+"\tACCESSORY:\t"+str(accessory)
			if line.startswith("#CHROM"):
				write_to_out = "body"
	infile.close()
	outfile.close()

main()
