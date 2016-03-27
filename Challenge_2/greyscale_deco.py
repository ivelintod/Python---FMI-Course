from functools import wraps


def greyscale(func):
    @wraps(func)
    def wrapper(matrix):
        res = func(matrix)
        for row in res:
            for ind, pix in enumerate(row):
                greysc = sum(pix) / len(pix)
                new_pix = tuple([int(greysc) for i in range(len(pix))])
                row[ind] = new_pix
        return res
    return wrapper
