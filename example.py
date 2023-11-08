import verify_calls

# Record the input params and outputs ot the file recording.log
v = verify_calls.Verify("RECORD", "recording")
@v.verify
def mul_by_x(lst, x):
    return [ item * x for item in lst ]
print(mul_by_x([1,2,3], 1))
print(mul_by_x([4,2], 3))

# same sequence, same input, same output --> verification should pass
v = verify_calls.Verify("VERIFY", "recording")
@v.verify
def mul_by_x(lst, x):
    return [ item * x for item in lst ]
print(mul_by_x([1,2,3], 1))
print(mul_by_x([4,2], 3))

# different way of wrapping the funciton - good for pre-defined functions, such a from C
v = verify_calls.Verify("VERIFY", "recording")
def mul_by_x(lst, x):
    return [ item * x for item in lst ]
mul_by_x = v.verify(mul_by_x)
print(mul_by_x([1,2,3], 1))
print(mul_by_x([4,2], 3))

# different sequence --> verification should fail
v= verify_calls.Verify("VERIFY", "recording")
@v.verify
def mul_by_x(lst, x):
    return [ item * x for item in lst ]
print(mul_by_x([4,2], 3))
print(mul_by_x([1,2,3], 1))

# different input params --> verification should fail
v = verify_calls.Verify("VERIFY", "recording")
@v.verify
def mul_by_x(lst, x):
    return [ item * x for item in lst ]
print(mul_by_x([1,3,3], 1))
print(mul_by_x([4,2], 3))

# different output  --> verification should fail
v = verify_calls.Verify("VERIFY", "recording")
@v.verify
def mul_by_x(lst, x):
    return [ item * x+1 for item in lst ]
print(mul_by_x([1,2,3], 1))
print(mul_by_x([4,2], 3))
