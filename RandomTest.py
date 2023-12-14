def sieve_of_eratosthenes(limit):
    primes = []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            primes.append(i)
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    for i in range(int(limit**0.5) + 1, limit + 1):
        if is_prime[i]:
            primes.append(i)

    return primes

def summation_of_primes(limit):
    primes = sieve_of_eratosthenes(limit)
    return sum(primes)

# Set the limit to 2 million
limit = 2000000
result = summation_of_primes(limit)

print(f"The summation of all prime numbers less than {limit} is: {result}")
