import random
import datetime

def get_random_latency(max_latency: int):
    """
    Selects from different probability distributions depending on the minute of the hour.
    For minutes (mod 10) less than 3, it uses a normal distribution for lower variance.
    For minutes (mod 10) less than 6 or greater, it uses an exponential distribution for higher variance.
    For all others it uses a uniform distribution between 0 and (max_latency * 0.01)s.

    max_latency caps the latency targeted means, the unit is "increments of 10 ms"
    """
    current_minute = datetime.datetime.now().minute % 10
    rate = 1 / (max_latency * 0.01)  # Mean latency of max_latency * 10ms for the exponential distribution

    if current_minute < 3:
        # Use a normal distribution with mean max_latency * 0.005 (for a peak around (max_latency * 5) ms)
        # and a std deviation that ensures most values are within the range of 0 to (max_latency * 10) ms
        delay = random.normalvariate(mu=max_latency * 0.005, sigma=0.02)
        # Clip the delay to a minimum of 0 and a maximum of max_latency * 10ms
        delay = max(min(delay, max_latency * 0.01), 0)
    elif current_minute < 6:
        # Use an exponential distribution
        delay = random.expovariate(rate)
        # Ensure delay does not exceed max latency (max_latency * 10ms)
        delay = min(delay, max_latency * 0.01)
    else:
        delay = random.randint(0, max_latency) * 0.01

    return delay
