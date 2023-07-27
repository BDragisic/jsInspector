import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog="jsInpector",
        description="A script to detect the versions of common JS libraries present on a webpage.",
        epilog="Developed by github.com/BDragisic and github.com/Gr4y-r0se",
    )

    parser.add_argument("-t", "--target", help="Specify a single webpage to scan")

    parser.add_argument(
        "-f",
        "--file",
        help="Specify path to file with a list of newline separated domains",
    )

    return parser.parse_args()

def get_libs():
    """
    Read the version commands from CSV file and add them to array which is interpolated into
    a Javascript function which executes them and returns an array in the console
    """
    array = []
    with open("./libraries.csv", "r") as infile:
        reader = [i.strip() for i in infile.readlines()]

    for row in reader:
        splitRow = row.split("|")
        name, command, npmLink = splitRow[0], splitRow[1], splitRow[2]

        nameLink = name + "|" + npmLink
        parsedCommand = (
            """"%s: ".concat(eval('try { %s } catch { "Not Present" }'))"""
            % (nameLink, command.strip())
        )

        array.append(parsedCommand)

    command = (
        """function results() {var results = [];
            var arr = %s;
            for (var lib in arr) {
            results.push(eval(arr[lib]));
            }
            return results;}; return results()"""
        % array
    )
    return command
    exit()