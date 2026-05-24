def _quick_pattern(two_theta, intensity):
    from matplotlib import pyplot as plt

    plt.figure(figsize=(6,4))
    plt.plot(two_theta, intensity, lw=1)
    plt.xlabel("2θ (degrees)")
    plt.ylabel("Intensity (a.u.)")
    plt.title("Simulated XRD Pattern")
    plt.tight_layout()
    plt.show()