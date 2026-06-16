def _quick_pattern(two_theta, intensity):
    from matplotlib import pyplot as plt

    fig, ax = plt.subplots(figsize=(6,4))

    ax.plot(two_theta, intensity, lw=1)
    ax.set_xlabel("2θ (degrees)")
    ax.set_ylabel("Intensity (a.u.)")
    ax.set_title("Simulated XRD Pattern")
    fig.tight_layout()
    plt.show()