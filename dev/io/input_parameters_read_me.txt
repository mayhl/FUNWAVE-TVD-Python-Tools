----------------------------------------------
Description of columns in input_parameters.csv
----------------------------------------------


Name	            - Parameter name in FUNWAVE input/driver file
Is Deprecated	    - True/False parameter is parameters is deprecated
FORTRAN Name	    - Relevant variable name in FUNWAVE FORTRAN for cases that differ from input/driver file
Full Name	    - Full name for clean display 
Datatype	    - Datatype enumeration for parameter 
			> Flag        : FORTRAN Compiler flag
                        > Integer     : Integer values
			> List        : Value in List or enumeration 
			> Boolean     : True/False value (T/F in FUNWAVE input/driver file)
			> Float       : Decimal number
			> Path        : Path to file containing data
			> String      : Arbitrary string value
			> Output Flag : Hacky solution for filtering out True/False parameter that control 
                                        individual or set of 2D field output(s).  
Module	            - 
Category	    - 
Units	            - Units of parameter 
Is Required	    - Is parameter required to run FUNWAVE
Default Value	    - Default value of parameter
Mask	            - Mask enumeration or list to validate parameter value. 
                       > Integer and Float datatypes  
	                  + None                : Only apply default datatype parsing and casting 
                          + 'Positive'          : Value greater than or equal to zero 
                          + 'Positive Definite' : Value greater than zero
                          + List of two values  : Upper and lower inclusive bounds for number
		       > List/Enum
                          + List of possible values
                       > Others:
                          + None: Only apply default datatype parsing and casting

Dependencies	    - String of parameter name this parameter is dependent on, or Python compatible list of parameter names. 
                      Note: Each dependency is treated as independent and only one dependency needs to be satisfied
Dependencies Values - Value or Python compatible list of values for parameter this parameter is dependent on. List of values or list of list 
Description         - Description of parameter


NOTE: Cells with list value will contain are assumed to contain the '[' character and be written as a Python 
      literal list definition, e.g. ['VAL1', 'VAL2', ...] for a list of strings, or
                                    [True, 'VAL1'] for a list contain a boolean and and string. 
