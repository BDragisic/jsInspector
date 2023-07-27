import requests
import json

from modules import banner,parse_args

from packaging import version
from termcolor import colored


if __name__ == "__main__":
    args = parse_args()
    print(
        banner
    )

    if args.target != None:
        targets = [args.target]
    elif args.file != None:
        with open(args.file, "r") as domainsFile:
            targets = [i.strip() for i in domainsFile.readlines()]

    for target in targets:
        target = target if "https" in target else "https://" + target

        print("\nTarget:", colored(f"{target}\n", "blue"))

        output = get_version(target)

        for library in output:
            # Janky splits but works for now
            nameAndLink = library.split(":")[0]
            name = nameAndLink.split("|")[0]
            npm = nameAndLink.split("|")[1]

            _version = library.split(":")[1]
            # If the package is avaiable on the NPM registry we can extract the latest version and compare
            if npm and _version != " Not Present" and _version != " undefined":
                latestVersion = json.loads(requests.get("https://" + npm.strip()).text)[
                    "version"
                ]

                if version.parse(_version) < version.parse(latestVersion):
                    colour = "red"
                    name = name + " OUTDATED"
                else:
                    colour = "green"

            else:
                latestVersion = None
                colour = "green"

            if _version != " Not Present" and _version != " undefined":
                print(f"    [*] {name}:")
                print(f"        [*] Version detected: " + colored(_version, colour))
                if latestVersion:
                    print(
                        f"        [*] Latest version: "
                        + colored(latestVersion, "green")
                    )
