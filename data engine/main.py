#pip install dtaidistance
#pip install numba
#pip install stumpy
import countriesIndex as ci
import patternEngine  as pe

def main():
    ci.countriesInit()
    ## Main Input
    path = r"C:\Users\NEW\Desktop\Projects\FIFADash\trojan\data bank\Cost of Living\Numbeo\Cost of Living Index.csv"
    outp = r"C:\Users\NEW\Desktop\Projects\FIFADash\trojan\data bank\Cost of Living\Numbeo\\"

    ## Find pattern between 2 time countries only
    #patternLen = 5
    #index      = "Legatum Prosperity Score"
    #names      = ["Peru", "Malaysia"]
    #dropCols   = ["Region"]
    #interval   = [] #[2007, 2013, 2014, 2021]
    #pe.findPattern2Countries(path, names, index, patternLen, interval, dropCols, debug = True)

    ### Find common patterns among an entire CSV    
    patternInterval = [3, 4, 5, 6, 7, 8, 9, 10]
    dropCols        = []
    res             = pe.findAllPatterns(path, outp, dropCols, patternInterval, fixYears = [".01", ".06"]) 
    pattsDF         = res[0]
    if len(res) > 1:
        dumpDF = res[1]
    
    ### Clean results for dashboard
    #dahsDF = pe.pattsToDashDF(pattsDF)

if __name__ == "__main__":
    main()