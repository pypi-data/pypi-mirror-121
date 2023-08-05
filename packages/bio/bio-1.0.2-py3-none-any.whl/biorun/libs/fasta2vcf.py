import os, sys
from Bio import SeqIO
import plac
sys.path.append(".")
from .utils import DefaultOrderedDict


def get_IDs_from_align_file(align_fn):
	ID = []
	for record in SeqIO.parse(align_fn, "fasta"):
		ID.append(record.id)
	if len(ID) > 2:
		print("Alignment file have >2 sequences. Using the first 2 sequences.")
	return ID[0], ID[1]

def parse_align(align_fn):
	ref = ""
	qry = ""
	n_record = 0
	with open(align_fn, "r") as f:
		for line in f:
			if line.startswith(">"):
				if n_record == 0:
					is_ref = True
					n_record += 1
				else:
					is_ref = False
			else:
				if is_ref:
					ref += line.strip()
				else:
					qry += line.strip()

	return ref, qry


def align2variant(ref, qry):
	assert len(ref) == len(qry)
	ref_coord = 0
	qry_coord = 0
	ref_variant = DefaultOrderedDict(str)
	qry_variant = DefaultOrderedDict(str)
	r0 = ""
	q0 = ""

	for r, q in zip(ref,qry):
		r = r.upper().replace("U", "T")
		q = q.upper().replace("U", "T")

		if r != "-":
			ref_coord += 1
		if q != "-":
			qry_coord = ref_coord

		if r != "-" and q != "-":
			r0 = r
			q0 = q

		if r == q:
			pass
		elif r == "n" or q == "n":
			pass
		elif r == "-":
			if ref_variant[ref_coord] == "":
				ref_variant[ref_coord] = r0
				qry_variant[ref_coord] = q0
			ref_variant[ref_coord] += r
			qry_variant[ref_coord] += q
		elif q == "-":
			if ref_variant[qry_coord] == "":
				ref_variant[qry_coord] = r0
				qry_variant[qry_coord] = q0
			ref_variant[qry_coord] += r
			qry_variant[qry_coord] += q
		elif r != q:
			ref_variant[ref_coord] = r
			qry_variant[ref_coord] = q
		else:
			raise Exception("Error! Please email your sequence to jollier.liu@gmail.com")
	return ref_variant, qry_variant


def save_vcf(ref_variant, qry_variant, qry_name, out_fn):
	assert len(ref_variant) == len(qry_variant)
	with open(out_fn, "w") as f:
		f.write('##fileformat=VCFv4.2\n')
		f.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
		f.write('##FILTER=<ID=PASS,Description="All filters passed">\n')
		f.write('##contig=<ID=NC_045512.2,length=29903,assembly=NC_045512.2>\n')
		f.write(f"#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t{qry_name}\n")
		for coord in ref_variant.keys():
			if coord == 0: # skip coord = 0
				continue

			rv = ref_variant[coord].replace("-","")
			qv = qry_variant[coord].replace("-","")

			rv_is_canonical = all([x in ["A","T","G","C"] for x in rv])
			qv_is_canonical = all([x in ["A","T","G","C"] for x in qv])

			if rv_is_canonical and qv_is_canonical:
				f.write(f"NC_045512.2\t{coord}\t.\t{rv}\t{qv}\t.\tPASS\t.\tGT\t1\n")


def filter_polya(vcf_fn):
	print("Removing variants in the Poly-A tail.")
	with open(vcf_fn, "r") as fin, open(f"{vcf_fn}.tmp", "w") as fout:
		for line in fin:
			if line.startswith("#"):
				fout.write(line)
			else:
				split_line = line.strip().split("\t")
				pos = split_line[1]
				ref = split_line[3]
				if pos == "29870" and ref.endswith("AAAAAAAAAA"):
					pass
				else:
					fout.write(line)
	os.remove(vcf_fn)
	os.rename(f"{vcf_fn}.tmp", vcf_fn)



def align2vcf(align_fn, qry_id):

	ref, qry = parse_align(align_fn)

	ref_variant, qry_variant = align2variant(ref, qry)

	save_vcf(ref_variant, qry_variant, qry_id)


def fasta2vcf(fname):

	# If user set align_fn option.
	ref_id, qry_id = get_IDs_from_align_file(fname)

	align2vcf(fname, qry_id)



@plac.opt("fasta", type=str, help="Input FASTA file.")
def main(fasta_fn):
	fasta2vcf(fasta_fn)

def run():
	plac.call(main)

if __name__ == "__main__":
	run()