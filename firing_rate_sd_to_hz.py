import sys

with open("results/base_mean_sd.txt", "r") as f:
    lines = f.readlines()

mean = float(lines[0].strip())
sd = float(lines[1].strip())

def fr_sd_to_hz(fr_sd):
    return int(round(mean + fr_sd * sd))

if __name__ == "__main__":
    fr_sd = float(sys.argv[1])
    print(fr_sd_to_hz(fr_sd))