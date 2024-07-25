# NOTE:
* Max char length is **5**
* Each "Page" can store at most 5 words
* Each Page can store **25 bytes** (5bytes(single char = 1 byte) * 5)
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



# What I have learnt

* "During the Database project, I have learnt buffering, cache, bitmap, bitwise operators such as ""&"", ""|"", ""~"", ""<<""and "">>"". Moreover, I have learnt clock policy for optimize buffering. I will go through one by one more in detail below.

## Buffering and cache
* Buffering is something you can think of like a spaceship going to Pluto. We do not want our spaceship going to ship a little items to it. Rather pack with full of items and send it all in one so that we can save energy. It is same idea so instead of storing data into database every single write, we can store into local memory and once the local memory is full, store it into database.

* cache is reusing pre-calculated result when same input was faced. During this project, I used cache for reading data if that data is in ""most frequently use"". I used clock policy for that and I will talk about it more in detail later

For designing database, I have to come up with how to store data efficiently. 
I have built 
1. Bitmap class(max size is 8 since 1byte = 8bits)
2. Page class
3. FileManager class(for checking how many times accessing DB)
4. PageBuffer, ClockBuffer classes


While I was building Bitmap, I have learnt what the bitmap is and why it is useful for building database. The reason for hiring bitmap is because it is easy to find which memories are full or empty. 
Let say, the database can store 1.space for size of bit map to find where the available memories are and 2.at most 7 items(each items are 1bit each). if we add an item called ""Taesu""  in bitmap class. the first 1bit of bitmap will indicate where the filled locations are. Therefore, reading in specific memory or writing into memory can be really efficient according to that map(T = O(1)). Also, I made this database can store fix length data since if the database can store random length items, it will be quite complicate to shift data when the data is removed and we cannot reuse empty space. For instance, we have 0 spots available among 8 spots in bitmap and remove 1 item called ""headphone"" which is 9 length word. Now 1 spot is available with 9 length. If we add ""grape"", 4 length worth spaces are waste. If we add ""United States of America"" instead, it won't fit in the spot as this word is longer than 9 length. On the other hand, If we only store fix length items, we can reuse same spot since all of data length are same. Which means we do not need to care about the data will fit in this spot or not. Because of this, I decided to use fixed length approach. 

I also learnt bit wise ""and"", ""or"", ""not"", and ""shift"". These operators are significantly powerful especially work in on lower level. Lets, look at from the bitwise ""and"".

* bitwise and ""&""
- bitwise and ""&"" is powerful operator when we want to find a free space in bitmap with specific index(0 to 7). it will only return 1 if both values are 1. Otherwise return 0. The use-case, for & operator is for instance, finding free space from bitmap. Let's say bitmap looks like binary 10000000 like this. We want to know first position has free space(start from left side and 1 means full and 0 means empty). The first position value is 1. Therefore, if we check first position, it will return 1(1 & 1 -> 1). If it returns 1, it means we are sure there's a value. Therefore, we can easily know that memory location is unavailable. 

* bitwise or ""|""
- Bitwise or ""|"" will return 1 if x and y values are both 0. Otherwise return 0. This operator is useful for updating bitmap. 

* bitwise not ""~""
- Bitwise or ""~"" will return opposite values of binary. For instance I have a value 2 in binary like this 00100. If I apply ""~"" operator, it will return ""11011"". It is useful for unsetting value from bitmap using with ""&"" operator. Let's unset value from bitmap. The logic is 
a. create a removing index value 1 which bitwise shift n times where n is equal to the index we want to unset value. 
b. create bitwise not value of removing index value.
c. use bitwise and operator for original value with removing index value for unset value. 

Let's see an example.
I have a value 10101 and want to unset index 2 value which is middle most ""1"". We can unset it like first, create a bitwise ""~"" version of 1 value which bitwise shift twice so that we can unset middle value.About bitwise shift, I will talk more in detail later but after bitwise shifting twice, it will looks like this 001. For just readability i will add two 0s at the end and looks like this 00100. From this value, apply logic ""b"", it will return like this 11011 for bitwise ""~"" value. Lastly, compare original value 10101 and ""~"" version of value 11011, the result looks like 10001. It is the unset version of original value 10101 and successfully unset middle ""1"" value. 

* bitwise shift ""<<"" or "">>""
- Bitwise shift is useful for finding free space in bitmap, set or unset value in bitmap. ""<<"" will shift value n times where n is equal to index to leftwards and "">>"" will shift rightward. For instance I have a value 1001 and if I ""<<"" twice, it will be 001001 and "">>"" for twice, it will return to 01

While I was making database, I realized how important creating unit tests are. The unit test makes sure the each unit of functions work as expected. I was underestimated the unit test so not creating the test and keeps building database classes and its methods. Once it got big enough. Suddenly some logic was broken. That time, it was too hard to debug where the bug was since I was not sure is each method works as expected. If I had a unit tests for at least some of methods, I am sure that at least those methods are working fine. Therefore, I could find other potential buggy area. After this incident, I started to create unit tests and each methods are more reliable. Also, I learnt creating mock classes are helpful for testing. When the logic of process getting complicated, it will be hard and cumbersome to create test case objects since one class wraps other class which wraps other class. However, if I create mock class which contains same method as expected class has, we can just test specific method and I can save lot more time and test can be specific yet precise. 

About the buffer logic, I used clock policy for optimize buffering. Clock policy is the optimized buffer. 
The logic is 
a. ""pool"" which size can be differ but say 6 contains data. The ""pool"" values are not stored in I/O but in local. When the user tries to retrieve data and pool contains it, we can return the value we stored in ""pool"". We do not need to access I/O device. However, if the data user looking for is not in the ""pool"", finally, we access to I/O. After the operation, replace ""oldest"" pool element with newly retrieved data. Each data in pool contains ""hand"" which pointing next data like as clock. Also contains reference bit property. Replace logic is if the current data's reference bit is off and current clock hand pointing to that data, we replace that data with new data. For instance, I have a values phone, book, headphone, and paper. The pointer looks like this [phone -> book -> headphone -> paper -> phone], each reference bit is True at first, and clock hand pointing to phone. When the user try to retrieve data ""pen"", pen doesn't exist in our pool so access to I/O and retrieve ""pen"". We need to replace pen with least frequently used value in pool. Start from phone since the clock hand points to it. As reference bit is True, update reference bit to be False and update clock hands pointing to book. However, again books reference bit is True, we need to update it to False and update pointer to next. Keeps doing it and when we reach phone again after paper, reference bit of phone is false and clock hand pointing to phone. Therefore, we will replace phone with pen. The pool looks like this [pen ->  book -> headphone -> paper -> pen] and clock hand pointing to book and return to updated index which is 0 where the replaced value phone was. In this way we can effectively replace least frequent value


