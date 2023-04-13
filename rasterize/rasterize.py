import os
from weights import layers


def main():
    input_dir = "extract"
    output_dir = "output"

    try:
        os.mkdir(output_dir)
    except FileExistsError:
        pass

    for layer in layers:
        layer.rasterize(input_dir=input_dir, output_dir=output_dir)


if __name__ == "__main__":
    main()
