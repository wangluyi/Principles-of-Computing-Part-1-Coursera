TEST_CASES = [1,66,34,46,678,5555]

def format(tenth):
    after=(tenth%600)/10.000
    before=tenth/100    
    return str(before)+':'+str(after)

for i in TEST_CASES:
    format(i)
