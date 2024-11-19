from pathlib import Path
import os
import re
import argparse

def extractNumber(string: str) -> int:
    """
    Extracts a number from a string and returns it.

    Parameters:
        string (str): The input string from which the number is to be extracted.

    Returns:
        int: an integer cast from the first index of the numbers list.
    """
    numbers: list = re.findall(r'\d+', string)
    return int(numbers[0])

def getBetterDirName(dirName: str) -> str:
    """
    Uses pattern matching to build the proper directory name and then returns it.

    Parameters:
        dirName (str): The original name of the directory

    Returns:
        str: A corrected directory name, or an empty string if a corrected name cannot be determined.
    """
    ### Add new patterns to check here ###
    patterns: list[str] = [
        r"S\d{2}",
        r"S\d{1}",
        r"S \d{2}",
        r"S \d{1}",
        r"Season\d{2}",
        r"Season\d{1}",
        r"Season \d{2}",
        r"Season \d{1}"
    ]

    for pattern in patterns:
        matches: list = re.findall(pattern, dirName)

        if matches:
            try:
                seasonNumber: int = extractNumber(matches[0]) # pass in the first index as findall returns a list
            except (IndexError, ValueError) as e:
                print(f"Error: Cannot extract integer from '{matches[0]}'. {e}")
                return ""

            return f"Season {seasonNumber}"

    return ""

def getBetterFileName(fileName: str, seasonNumber:int) -> str:
    """
    Uses pattern matching to build the proper file name and then returns it.

    Parameters:
        fileName (str): The original name of the file.
        seasonNumber (int): The season number for the current directory.
            As this is determined before the file is passed here, there is no need to extract it from the filename.

    Returns:
        str: A corrected file name, or an empty string if a corrected name cannot be determined.
    """
    suffix: str = fileName.split('.')[-1]

    ### Add new patterns to check here ###
    patterns: list[str] = [
        r"E\d{2}",
        r"E\d{1}",
        r"E \d{2}",
        r"E \d{1}",
        r"Episode \d{2}",
        r"Episode \d{1}",
        r"e\d{2}",
        r"e\d{1}",
        r"e \d{2}",
        r"e \d{1}",
        r"episode \d{2}",
        r"episode \d{1}"
    ]

    for pattern in patterns:
        matches = re.findall(pattern, fileName)

        if matches:
            try:
                episodeNumber = extractNumber(matches[0])
            except (IndexError, ValueError) as e:
                print(f"Error: Cannot extract integer from '{matches[0]}'. {e}")
                return ""

            # As the episode nomenclature here is S##E##, here is the 4-piece if block
            if (episodeNumber < 10 and seasonNumber < 10):
                return f"S0{seasonNumber}E0{episodeNumber}.{suffix}"

            elif (episodeNumber < 10 and seasonNumber > 10):
                return f"S{seasonNumber}E0{episodeNumber}.{suffix}"

            elif (episodeNumber > 9 and seasonNumber < 10):
                return f"S0{seasonNumber}E{episodeNumber}.{suffix}"

            else:
                return f"S{seasonNumber}E{episodeNumber}.{suffix}"

    return ""


def main():
    parser = argparse.ArgumentParser(description="Process a directory path.")
    parser.add_argument('directory', type=str, help="Path to the directory")

    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        return
    else:
        path = Path(args.directory)

    for dirpath, dirnames, filenames in os.walk(path):
        correctDirName: str = getBetterDirName(dirpath)

        # skip if dir name does not match 
        if not correctDirName:
            continue

        seasonNumber = int(correctDirName.split(" ")[-1])
        if os.path.realpath(path) == os.path.realpath(dirpath):
            newDirPath = Path(correctDirName)
        else:
            newDirPath = Path(path) / Path(correctDirName)

        for file in filenames:
            oldPath: Path = Path(dirpath) / Path(file)
            newName: str = getBetterFileName(file, seasonNumber)
            if newName:
                newPath: Path = Path(dirpath) / Path(newName)
                os.rename(oldPath, newPath)
                print(f"Renamed: {oldPath} -> {newPath}")

        if newDirPath:
            os.rename(dirpath, newDirPath)
            print(f"Renamed: {dirpath} -> {newDirPath}")

if __name__ == "__main__":
    main()
