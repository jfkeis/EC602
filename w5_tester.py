# -*- coding: utf-8 -*-
"""
# AUTHOR John Keisling jfkeis@bu.edu
# AUTHOR Sigurdur Egill Thorvaldsson sigurdur@bu.edu

w5_testpoly.py
10/2/16
Siggi&John
"""

import unittest
import importlib
import glob
import io
import sys
import json

import w5_testpoly

suppress_output = False

def check_all_files():
    passed,failed = [],[]

    Trials = glob.glob('poly*.py')

    for file_name in Trials:
        loader = unittest.loader.TestLoader()
        results = unittest.result.TestResult()

        try:
            
            print("here")
            if suppress_output:
                s = io.StringIO()
                sys.stdout = s

            module_tested = importlib.import_module(file_name[:-3])
            w5_testpoly.Polynomial = module_tested.Polynomial
            tests = loader.loadTestsFromTestCase(w5_testpoly.PolynomialTestCase)
            tests.run(results)

            tests_passed = results.testsRun - len(results.failures) - len(results.errors)     
  
            if results.wasSuccessful():
                passed.append(file_name) 
            else:
                failed.append(file_name)   
            if suppress_output:
                sys.stdout = sys.__stdout__
    
            print('Run {} tests'.format(results.testsRun))
            
            
            print('you passed {} tests'.format(tests_passed))
            for test,output in results.failures:
                 print(">>",test)
                 print(">>",output)
            for test,output in results.errors:
                 print(">>",test)
                 print(">>",output)
             
        except Exception as e:
            if suppress_output:
                sys.stdout = sys.__stdout__

            print('exception',file_name,e)
            failed.append(file_name)

    return passed,failed

if __name__ == "__main__":
    passed,failed = check_all_files()
    Results={'failed':failed,'passed':passed,'authors':w5_testpoly.authors}
    with open('week5_results.json','w') as f:
        json.dump(Results,f,indent=4)
