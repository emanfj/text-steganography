# Text Steganographic Technique for Data Hiding

## 1. Encode secret information
The `encode()` function works in the following way:
* Formats given secret text into binary.
* Uses the non-printable Zero Width Joiners (to represent 1) and Zero Width Non Joiners (to represent 0) to hide the binary data between character spaces.
* Outputs the steganographic data to a new file.