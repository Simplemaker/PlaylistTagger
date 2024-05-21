# Playlist Tagger

Download, tag, and add art to a playlist using a simple key-value pair format.

Example input:
```
title: Song to Listen To
yt: https://www.youtube.com/watch?v=...
art: https://example.org/image.jpg
artist: Artist
track: 5

title: Second Song to Listen to ...
```

Song requests are separated by a double newline. Using 
`art: thumbnail` will download the thumbnail art as the
album art.
