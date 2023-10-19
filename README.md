# 2023.8/3 18:32

self.readCount:65, self.seekCount:76, self.writeCount:11
Case pageBuffer

```
self.readCount:7, self.seekCount:22, self.writeCount:15
```

# Video Links

- https://www.youtube.com/@CS186Berkeley/playlists
- https://cs186berkeley.net/

# Create database from scratch

## Current Progress

- Understood what is bit map
- Learnt man command
  - ```
    man ascii
    ```

* Pros and Cons of Bitmap

  **Pros**

  - Able to find empty space quickly
  - No need to reorganize order after delete operation

  **Cons**

  - Maximum storage is up to 8 slot items

- 1 byte = 8 bits

- ASCII characters are 7bit word
- Bitwise operators(https://wiki.python.org/moin/BitwiseOperators)
  - **~** : Bitwise not
  - **>>** or **<<** : Bitshift
  - **|** : Bitwise or
  - **&** : Bitwise and

* Cache and Buffering

* - Cache is the one re-use pre-calculated result when same input is coming
* - Buffering is like going to pluto. Instead of sending data one by one, sending at the same time when the data is full
