# foobar2000StartTimeTag
Python Script that creates a start time tag for mp3, flac etc. files in an album.

## Usage
The script contains 4 "global" variables at the top to easily influence behaviour.
| variale      | usage                                                                 |
|--------------|-----------------------------------------------------------------------|
| music_folder | Path to Folder with the music files (will be searched rekursively)    |
| file_types   | default: All supported file Types. Others may or may not be supported |
| album_keys   | what defines an album; default: albumartist and alum                  |
| tag_name     | name of the created tag                                               |

## Dependencies
music-tag (Used to read/ write tags)
tinytag (Used as "Backup" source for duration)
