from ._helpers import isochoric_volumetric_split
from ..math import det, transpose, trace, eigvals, sum1


def saint_venant_kirchhoff(F, mu, lmbda):
    C = transpose(F) @ F
    I1 = trace(C) / 2 - 3 / 2
    I2 = trace(C @ C) / 4 - trace(C) / 2 + 3 / 4
    return mu * I2 + lmbda * I1 ** 2 / 2


@isochoric_volumetric_split
def neo_hooke(F, C10):
    C = transpose(F) @ F
    I1 = trace(C)
    return C10 * (I1 - 3)


@isochoric_volumetric_split
def mooney_rivlin(F, C10, C01):
    C = transpose(F) @ F
    I1 = trace(C)
    I2 = (trace(C) ** 2 - trace(C @ C)) / 2
    return C10 * (I1 - 3) + C01 * (I2 - 3)


@isochoric_volumetric_split
def yeoh(F, C10, C20, C30):
    J = det(F)
    C = transpose(F) @ F
    I1 = J ** (-2 / 3) * trace(C)
    return C10 * (I1 - 3) + C20 * (I1 - 3) ** 2 + C30 * (I1 - 3) ** 3


@isochoric_volumetric_split
def third_order_deformation(F, C10, C01, C11, C20, C30):
    C = transpose(F) @ F
    I1 = trace(C)
    I2 = (trace(C) ** 2 - trace(C @ C)) / 2
    return (
        C10 * (I1 - 3)
        + C01 * (I2 - 3)
        + C11 * (I1 - 3) * (I2 - 3)
        + C20 * (I1 - 3) ** 2
        + C30 * (I1 - 3) ** 3
    )


@isochoric_volumetric_split
def ogden(F, mu, alpha):
    C = transpose(F) @ F
    wC = eigvals(C)

    out = 0
    for m, a in zip(mu, alpha):
        wk = wC ** (a / 2)
        out += m / a * (sum1(wk)[0, 0] - 3)

    return out


@isochoric_volumetric_split
def arruda_boyce(F, C1, limit):
    C = transpose(F) @ F
    I1 = trace(C)

    alpha = [1 / 2, 1 / 20, 11 / 1050, 19 / 7000, 519 / 673750]
    beta = 1 / limit ** 2

    out = 0
    for i, a in enumerate(alpha):
        j = i + 1
        out += a * beta ** (2 * j - 2) * (I1 ** j - 3 ** j)

    return C1 * out
