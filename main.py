# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from Utilities.incident_angle import WaveAnalyzer


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wav_path = '/Users/akosborbath/Documents/Soundskrit/DA/DA_SKRT/Utilities/test_sound.wav'  # Replace with your WAV file path
    analyzer = WaveAnalyzer(wav_path)
    analyzer.play()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
