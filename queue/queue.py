import math

def prob_at_least_n(p, n, prob_n_in_system):
    other_p = 0
    n -= 1
    while n >= 0:
        other_p += prob_n_in_system(p, n)
        n -= 1
    return 1 - other_p

def prob_at_most_n(p, n, prob_n_in_system):
    return 1 - prob_at_least_n(p, n, prob_n_in_system) + prob_n_in_system(p, n)

class InfiniteQueue:
    def prob_zero_in_system(p, *args):
        return 1 - p

    def prob_n_in_system(p, n):
        return math.pow(p, n) * (1 - p)

    def length_of_system(p, *args):
        return p / (1 - p)

    def length_of_queue(p, *args):
        return InfiniteQueue.length_of_system(p) - p

    def wait_time_of_system(p, arrival_rate, *args):
        return InfiniteQueue.length_of_system(p) / arrival_rate

    def wait_time_of_queue(p, arrival_rate, *args):
        return InfiniteQueue.length_of_queue(p) / arrival_rate

class FiniteQueue:
    def prob_zero_in_system(p, n):
        return (1 - p) / (1 - math.pow(p, n + 1))
    
    def prob_n_in_system(p, n):
        return math.pow(p, n) * FiniteQueue.prob_zero_in_system(p, n)
    
    def length_of_system(p, n):
        x = n * math.pow(p, n+1)
        y = (n+1) * math.pow(p, n)
        w = 1 - p
        z = 1 - math.pow(p, n+1)
        return (p * (1 + x - y)) / (w * z)
    
    def eff_rate(arrival_rate, p, n):
        return arrival_rate * (1 - FiniteQueue.prob_n_in_system(p, n))
    
    def length_of_queue(p, n, arrival_rate, service_rate):
        return (
            FiniteQueue.eff_rate(arrival_rate, p, n) 
            * FiniteQueue.wait_time_of_queue(p, arrival_rate, service_rate, n))

    def wait_time_of_system(p, arrival_rate, n):
        return FiniteQueue.length_of_system(p, n) / FiniteQueue.eff_rate(arrival_rate, p, n)

    def wait_time_of_queue(p, arrival_rate, service_rate, n):
        return FiniteQueue.wait_time_of_system(p, arrival_rate, n) - (1 / service_rate)


if __name__ == "__main__":
    arrival_rate = float(input("arrival rate: "))
    service_rate = float(input("service rate: "))
    n = int(input("No of people: "))
    p = arrival_rate / service_rate
    q_type = input("is the queue finite? (y for yes, anything else for no): ")

    if q_type == "y":
        calcs = FiniteQueue
    else:
        calcs = InfiniteQueue
    print("Probability of", n, "people in the system:", calcs.prob_n_in_system(p, n))
    print("Length of the system:", calcs.length_of_system(p, n))
    print("Length of the queue:", calcs.length_of_queue(p, n, arrival_rate, service_rate))
    print("Wait time of the system:", calcs.wait_time_of_system(p, arrival_rate, n))
    print("Wait of queue:",  calcs.wait_time_of_queue(p, arrival_rate, service_rate, n))
    print("Probability of zero:", calcs.prob_zero_in_system(p, n))
