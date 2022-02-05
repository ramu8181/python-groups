class Solution:
    def romanToInt(self, s: str) -> int:
        result = 0
        values = {
			"I": 1,
			"V": 5,
			"X": 10,
			"L": 50,
			"C": 100,
			"D": 500,
			"M": 1000,
			# Substraction letters
			"Q": 4,
			"W": 9,
			"E": 40,
			"R": 90,
			"T": 400,
			"Y": 900,
		}
        replacements = {
            "IV" : "Q",
            "IX" : "W",
            "XC" : "R",
            "XL": "E",
            "CD" : "T",
            "CM" : "Y"
        }
        for pair in replacements:
            s = s.replace(pair, replacements[pair])
        
        for each in s:
            result += values[each]
        return result
            
        
