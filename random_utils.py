import random
import datetime

def get_random_latency():
    """
    Selects from different probability distributions depending on the minute of the hour.
    For minutes (mod 10) less than 3, it uses a normal distribution for lower variance.
    For minutes (mod 10) less than 6 or greater, it uses an exponential distribution for higher variance.
    For all others it uses a uniform distribution between 0 and 3s.
    """
    current_minute = datetime.datetime.now().minute % 10
    rate = 1 / 0.11  # Mean latency of 110ms for the exponential distribution

    if current_minute < 3:
        # Use a normal distribution with mean 0.055 (for a peak around 55ms) and a std deviation
        # that ensures most values are within the range of 0 to 0.11
        delay = random.normalvariate(mu=0.055, sigma=0.02)
        # Clip the delay to a minimum of 0 and a maximum of 110ms
        delay = max(min(delay, 0.11), 0)
    elif current_minute < 6:
        # Use an exponential distribution
        delay = random.expovariate(rate)
        # Ensure delay does not exceed max latency (110ms)
        delay = min(delay, 0.11)
    else:
        delay = random.randint(0, 300) * 0.01

    return delay
