#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on  10 08 21:23:14  2023

@Author: Lulu Shi

@Mails: crazzy_rabbit@163.com
"""

import click
import numpy as np
import pandas as pd
from numpy.linalg import eig

@click.command()
@click.option('--covfile', help=".cov file generated by pcAngsd", required=True)
@click.option('--pc', help="the number of pc to out", default=5)
@click.option('--outprefix', help="outfile prefix")
def main(covfile, pc, outprefix):
    """
    trans .cov file out from pcAngsd to eigenvec file
    """
    cov = np.genfromtxt(covfile)
    eigenvalues, eigenvectors = eig(cov)
    sumval = np.sum(eigenvalues)
    eigenvec = eigenvectors.T[eigenvalues.argsort()[::-1]] #转置，每列是一个vec
    eigenval = np.sort(eigenvalues)[::-1][:pc]
    pcs = {}
    for i in range(pc):
        exp = eigenval[i] / sumval
        pcs[f'PC{i+1}({exp*100:.2f}%)'] = eigenvec[i]
    pd.DataFrame(pcs).to_csv(f'{outprefix}.txt',idex=False, sep='\t')

if __name__ == '__main__':
    main()