from collections import defaultdict


def rotate_left(img):
    rotated = zip(*(r[::-1] for r in img))
    return list(rotated)


def rotate_right(img):
    rotated = zip(*(r for r in img))
    return list(rotated)


def invert(img):
    inverted = [[tuple([255 - el for el in pix])
                for pix in row]
                for row in img]

    return inverted


def lighten(img, coef):
    lightened = [[tuple([int(el + coef*(255 - el)) for el in pix])
                 for pix in row]
                 for row in img]

    return lightened


def darken(img, coef):
    darkened = [[tuple([int(el - coef*(el - 0)) for el in pix])
                for pix in row]
                for row in img]

    return darkened


def create_histogram(img):
    histogram = {}
    temp = defaultdict(int)
    keys = ('red', 'green', 'blue')
    for ind, key in enumerate(keys):
        for row in img:
            for pix in row:
                temp[pix[ind]] += 1
        histogram[key] = temp
        temp = defaultdict(int)
    return histogram


def main():
    image = [
            [(0, 0, 255), (0, 255, 0), (0, 0, 255)],
            [(255, 0, 0), (0, 0, 255), (0, 255, 0)],
            [(0, 255, 0), (0, 255, 0), (255, 0, 0)]]
    print(rotate_left(image))
    print(rotate_right(image))
    print(invert(image))
    print(lighten(image, 0.5))
    print(darken(image, 0.5))
    print(create_histogram(image))

if __name__ == '__main__':
    main()
