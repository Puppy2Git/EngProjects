num = 600851475143
def is_prime(n):
  i = n - 1
  des = True
  while i > 1:
    if (n % i == 0):
      des = False
      break
    i = i - 1
  return des
cantbe = False
primes = []
while (cantbe == False):
  index = num - 1
  foundit = False
  while (foundit == False):
    if (index == 1):
      if (is_prime(num)):
        primes.append(int(num))
        print(num)    
      cantbe = True
      break
    if (num % index == 0):
      if (is_prime(index)):
        num = num / index
        primes.append(int(index))
        print(index)
        foundit = True
    index = index - 1
print(primes)