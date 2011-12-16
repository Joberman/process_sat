'''
Interactive value-fetching class
Please, please, please replace me...
'''

def get_val_instr():
    '''Display instructions to user for get_val'''
    print("\nPress enter to accept value in parentheses.\n")
def get_val(default, prompt, limFunc=(lambda x: True), cast=(lambda x: x)):
    '''
    Get a value from the user using prompt.

    If the user presses enter w/o entering anything,
    the default value is returned.  These instructions
    are contained in get_val_instr().
    
    cast represents how the answer is cast before being
    checked by limFunc/returned.  It should be a callable
    that casts the input.  If cast is not passed, a string
    is returned.
    
    limFunc, if given, represents a limit on valid values.
    It should return True for valid values, False otherwise.
    It checks all values that would be output, including
    the default.  If no limFunc is given, all values that
    cast correctly are allowed.
    '''
    msg = prompt+' (s): ' % str(default)
    err = "Invalid input.  Please try again."
    while True:
        ans = raw_input(msg)
        try:
            ans = cast(ans)
        except(AttributeError, TypeError):
            print(err)
            continue
        if limFunc(ans):
            return ans
        print(err)

def get_yn(prompt):
    '''
    Get an answer of yes or no from user

    returns 'y' or 'n'
    '''
    while True:
        answer = raw_input(prompt)
        if answer in ['Y', 'y', 'n', 'N']:
            return answer.lower()
        print("Answer must be y or n.")

