# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on 05 08 10:52:08 2024
@Author: Lulu Shi
@Mails: crazzy_rabbit@163.com
"""

import click

def get_chr_mapping(chrlist_file):
    """按需获取染色体映射关系"""
    chr_mapping = {}
    with open(chrlist_file, 'r') as f:
        for line in f:
            old_chr, new_chr = line.strip().split()
            chr_mapping[old_chr] = new_chr
            chr_mapping[new_chr] = old_chr  # 确保双向映射
    return chr_mapping

@click.command()
@click.option('-i', '--infile', type=click.Path(exists=True), help='Input VCF file to change chromosome.', required=True)
@click.option('-c', '--chrlist', type=click.Path(exists=True), help='List of chromosomes to change, format: old_chr new_chr.', required=True)
@click.option('-o', '--out', type=click.Path(), help='Output file.', required=True)
def main(infile, chrlist, out):
    chr_mapping = get_chr_mapping(chrlist)
    
    with open(infile, 'r') as vcf_file, open(out, 'w') as outfile:
        header_lines_processed = False
        
        for line in vcf_file:
            line_strip = line.strip()
            if line_strip.startswith('#'):
                if not line_strip.startswith('##contig') or header_lines_processed:
                    outfile.write(line)
                else:
                    header_lines_processed = True
                    contig_info = line_strip.split('=', 3)
                    contigs = contig_info[2].strip().split(',')
                    updated_contigs = [chr_mapping.get(chr_, chr_) for chr_ in contigs]
                    if updated_contigs: # 只有当有更新时才写入
                        outfile.write(f'{contig_info[0]}={contig_info[1]}={",".join(updated_contigs)}={contig_info[3]}\n')
            else:
                parts = line_strip.split('\t')
                chrom = parts[0]
                if chrom in chr_mapping:
                    parts[0] = chr_mapping[chrom]  # 直接替换染色体名称
                    outfile.write('\t'.join(parts) + '\n')

if __name__ == '__main__':
    main()
