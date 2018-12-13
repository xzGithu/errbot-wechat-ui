l1=[1,2,3,4,5]
def gg(l1):
    for i in l1:
        if i==4:
            print ("yes")
            return 'eee'

            # break
            # return "find"

        print ("no")
        # break
    else:
        print ("no1")
print (gg(l1))