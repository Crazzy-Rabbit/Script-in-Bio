#! /bin/bash
# author: Shill
################ CNVCaller for genome data ##############
# Run this program in your bam file directory
# The format of the bam file should be .sorted.addhead.markdup.bam
# 800 in step 1 should change same as your Dup file window size


# Set up the file name(obtain the absolute paths), software                                             
CNVReferenceDB.pl="/home/sll/miniconda3/CNVcaller/bin/CNVReferenceDB.pl"                  #change as you want
Individual.Process.sh="/home/sll/miniconda3/CNVcaller/Individual.Process.sh"              #change as you want
CNV.Discovery.sh="/home/sll/miniconda3/CNVcaller/CNV.Discovery.sh"                        #change as you want
Genotype.py="/home/sll/miniconda3/CNVcaller/Genotype.py"                                  #change as you want
genomic.fna="/home/sll/genome-cattle/ARS-UCD1.2/GCF_002263795.1_ARS-UCD1.2_genomic.fna"   #Reference genome fa file, change as you want
Btau5.0.1_800_link="/home/sll/miniconda3/CNVcaller/Btau5.0.1_800_link"                    #dup file that you have created use blasr, change as you want

export PYTHONPATH="/home/sll/miniconda3/bin:$PYTHONPATH"                                  #Python3 path you set
echo $CNVReferenceDB.pl
echo $genomic.fna
echo $Individual.Process.sh
echo $Btau5.0.1_800_link
echo $CNV.Discovery.sh
echo $Genotype.py

# Create a window file for the genome (you can use it directly later)
perl $CNVReferenceDB.pl $genomic.fna -w 800

# Calculate the absolute copy number  of each window
bam=`ls *bam|cut -d"." -f 1 | sort -u`
for i in $bam;
	do 
	bash $Individual.Process.sh -b `pwd`/$bam.sorted.addhead.markdup.bam -h $bam -d $Btau5.0.1_800_link -s none;
	done    

cp referenceDB.800 RD_normalized
cd RD_normalized
ls -R `pwd`/*sex_1 > list.txt
touch exclude_list

# Determin the CNV region
bash $CNV.Discovery.sh -l `pwd`/list.txt -e `pwd`/exclude_list -f 0.1 -h 1 -r 0.1 -p primaryCNVR -m mergeCNVR

# Genotype determination
python $Genotype.py --cnvfile mergeCNVR --outprefix genotypeCNVR --nproc 8
echo "CNVCaller finished!"
