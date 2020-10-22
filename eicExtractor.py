import os, sys, pymzml, argparse
import numpy as np

DEFAULT_EXTRACTION_WIDTH = 0.01

parser = argparse.ArgumentParser(
    description = 'Extract chromatographic data from mzML files'
)

parser.add_argument('mzmlFile',
                    type = str,
                    help = 'File path of mzML data files. To specify multiple mzML files, include multiple \
                            argument/value pairs. For example --mzmlFile sample1.mzML --mzmlFile sample2.mzML \
                            --mzmlFile sample3.mzML'
                    )

parser.add_argument('eicTarget',
                    type = float,
                    help = 'Target ion for chromatogram plotting.'
                    )

parser.add_argument('--eicWidth',
                    default = DEFAULT_EXTRACTION_WIDTH,
                    type = float,
                    help = 'Width (in m/z) used to produce EIC plots'
                    )


def getEICData(options):

    targetLL = options.eicTarget - options.eicWidth
    targetHL = options.eicTarget + options.eicWidth

    print('Processing %s' %options.mzmlFile)

    print('EIC target: %s' %options.eicTarget)
    print('EIC target LL: %s' %targetLL)
    print('EIC target HL: %s' %targetHL)

    ofx = open('EIC_%s_%s.txt' %(
        options.eicTarget,
        options.mzmlFile.split('.')[0]
    ), 'wt')

    ofx.write('#RT\tIntensity\n')

    spectra = pymzml.run.Reader(options.mzmlFile)
    for s in spectra:

        if s.ms_level != 1: continue
        time = s.scan_time_in_minutes()
        mzs = s.mz
        ints = s.i

        mask = np.where( (mzs > targetLL) & (mzs < targetHL) )
        intsubset = ints[mask]

        ofx.write('%s\t%s\n'%(time, np.sum(intsubset)))
    ofx.close()

    return

def main(options):
    getEICData(options)

if __name__ == '__main__':
    options =  parser.parse_args()
    main(options)
