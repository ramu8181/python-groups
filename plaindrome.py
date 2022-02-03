class Solution:
    def isPalindrome(self, x: int) -> bool:
        str1 = list(str(x))
        val = len(str1)
        for i in range (0,val):
            if str1[i]==str1[val-i-1]:
                continue
            else:
                return ("no")
        return ("yes")


if __name__=='__main__':
    x= -121
    p = Solution()
    print (p.isPalindrome(x))
