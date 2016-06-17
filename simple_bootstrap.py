"""
Description of program
"""
import numpy as np


# ==============================================================================
# Define functions
# ==============================================================================
def bootstrap(F, N, array, err_array, *args, **kwargs):
    """

    :param F: function, the function to bootstrap around
              (first argument must be the bootstrapped version of array all
               other arguments taken in as *args and **kwargs)

    :param N: int, number of bootstrap iterations

    :param array: numpy array to bootstrap around must be the first argument
                  of F

    :param err_array: numpy array of uncertainties for array
                      (same shape as array)

    :param args: any other arguments passed to F

    :param kwargs: any keyword arguments passed to F

    :return:
    """
    # work out samples
    samples = np.random.normal(array, err_array, size=(N, len(array)))
    # work out function across parameters
    values = [F(samples[i], *args, **kwargs) for i in xrange(N)]
    # work out percentiles
    med, low, high = np.percentile(values, [50, 16, 84])
    # return 50th +- uncertainties
    return med, high - med, med - low


# ==============================================================================
# Start of code
# ==============================================================================
if __name__ == '__main__':
    # Test code make distribution of points following a linear trend
    x = np.random.normal(5.0, 2.0, 100)
    ex = abs(np.random.normal(0.0, 2.0, 100))
    # assign a function
    F = np.median
    # work out true value
    truevalue = F(x)
    # do bootstrap
    y, eyl, eyu = bootstrap(F, 10000, x, ex)
    # plot outcome
    import matplotlib.pyplot as plt
    plt.close()
    plt.errorbar(range(len(x)), x, yerr=ex, linestyle='', marker='o')
    tstr = 'True = ${0:.5f}$    Boot = ${1:.5f}^{{ +{2:.5f} }}_{{ -{3:.5f} }}$'
    targs = [truevalue, y, eyu, eyl]
    plt.title(tstr.format(*targs))
    plt.hlines(truevalue, 0, len(x), colors='g', linestyles='solid',
               label='True Value')
    plt.hlines(y, 0, len(x), colors='r', linestyles='solid', label='Boot value')
    plt.hlines([y+eyu, y-eyu], 0, len(x), colors='r', linestyles='dashed',
               label=r'Boot $\pm$ std')
    plt.legend(loc=0)
    plt.show()
    plt.close()

# ==============================================================================
# End of code
# ==============================================================================
