# Model for PII Detection

## Methodology

PII are detected from string using 2 ways
1) We use REGEX to extract PII which always follow a fixed pattern such as email address, IP address, Aadhar Number, etc.
2) We use NER to extract PII such as Person name, Location, and Organization

## Sample Input & Output

Input: `I live in Jelum Towers, Vice City, 400809, and I go by Sonny. I had an amazing drive through Vice City's neon-lit streets before heading to the storied Malibu Club for an exciting night of music that will never be forgotten. I'm constantly in awe of the city's breathtaking skyline and lively nightlife. Lance Vance, a buddy of mine, will see me shortly to discuss a mission. He is employed with The Dockyards. Using the IP address 172.182.99.1, he emailed me about the mission using the email address lancevance@gmail.com. A message from +919999999999 reached me as well. It appears to be authentic.`

Output: `2024-09-08 18:13:21,771 - INFO - Detected PII: [['lancevance@gmail.com', 'EMAIL'], ['172.182.99.1', 'IP'], ['919999999999', 'PHONE'], ['400809', 'PINCODE'], ['Jelum Towers', 'LOC'], ['Vice City', 'LOC'], ['Sonny', 'PER'], ['Vice City', 'LOC'], ['Malibu', 'ORG'], ['Club', 'LOC'], ['Lance Vance', 'PER'], ['The Dockyards', 'ORG']]`

## To Do

* PII detection from CSV and SQL dumps
* Binning of PII in categories like Biological, Financial, and Personal
* Better PII detection