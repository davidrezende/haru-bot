print(sum([x**2 for x in range(20)]))

x= 4
y = 2


if x := 1 != y :
  print(x)



import re

texto = "abc 12 3abc123abc12 3gdv234"
noNumber = re.compile(r'[^ \d]\D+')
print(noNumber.findall(texto))
