
# The MNIST database
The MNIST database of handwritten digits, available from this page, has a training set of 60,000 examples, and a test set of 10,000 examples. It is a subset of a larger set available from NIST. The digits have been size-normalized and centered in a fixed-size image.
It is a good database for people who want to try learning techniques and pattern recognition methods on real-world data while spending minimal efforts on preprocessing and formatting.

# Get the Data

Many ML libraries already include Fashion-MNIST data/API, give it a try!

You can use direct links to download the dataset. The data is stored in the same format as the original MNIST data.

Name	Content	Examples	Size	Link	MD5 Checksum
train-images-idx3-ubyte.gz	training set images	60,000	26 MBytes	Download	8d4fb7e6c68d591d4c3dfef9ec88bf0d
train-labels-idx1-ubyte.gz	training set labels	60,000	29 KBytes	Download	25c81989df183df01b3e8a0aad5dffbe
t10k-images-idx3-ubyte.gz	test set images	10,000	4.3 MBytes	Download	bef4ecab320f06d8554ea6380940ec79
t10k-labels-idx1-ubyte.gz	test set labels	10,000	5.1 KBytes	Download	bb300cfdad3c16e7a12a480ee83cd310
Alternatively, you can clone this GitHub repository; the dataset appears under data/fashion. This repo also contains some scripts for benchmark and visualization.

git clone git@github.com:zalandoresearch/fashion-mnist.git


# Labels
Each training and test example is assigned to one of the following labels:

Label	Description
0	T-shirt/top
1	Trouser
2	Pullover
3	Dress
4	Coat
5	Sandal
6	Shirt
7	Sneaker
8	Bag
9	Ankle boot

# Interpret a buffer as a 1-dimensional array.

numpy.frombuffer(buffer, dtype=float, count=-1, offset=0)¶

# Parameters:
* buffer: buffer_like
* An object that exposes the buffer interface.

# dtype: data-type, optional
* Data-type of the returned array: 
- int8 Byte (-128 to 127)

* default: float.

# count: int, optional
* Number of items to read. -1 means all data in the buffer. ALL THE BUFFER

# offset: int, optional
* Start reading the buffer from this offset(in bytes) default: 0.  
- offset=8


# reshape(len(y_train), 28, 28)
* redimentionne l'imaghe en 28x28

# Training 

## Training Labels

[offset] [type]          [value]          [description] 
0000     32 bit integer  0x00000801(2049) magic number (MSB first) 
0004     32 bit integer  60000            number of items 
0008     unsigned byte   ??               label --> We are here: offset 8 byte of Buffer
0009     unsigned byte   ??               label 
........ 
xxxx     unsigned byte   ??               label


## Training Image

[offset] [type]          [value]          [description] 
0000     32 bit integer  0x00000803(2051) magic number 
0004     32 bit integer  60000            number of images 
0008     32 bit integer  28               number of rows 
0012     32 bit integer  28               number of columns 
0016     unsigned byte   ??               pixel --> We are here: offset 16 byte of Buffer
0017     unsigned byte   ??               pixel 
........ 
xxxx     unsigned byte   ??               pixel


# Testing 

## TEST SET LABEL FILE 
[offset] [type]          [value]          [description] 
0000     32 bit integer  0x00000801(2049) magic number (MSB first) 
0004     32 bit integer  10000            number of items 
0008     unsigned byte   ??               label 
0009     unsigned byte   ??               label 
........ 
xxxx     unsigned byte   ??               label
The labels values are 0 to 9.

## TEST SET IMAGE FILE
[offset] [type]          [value]          [description] 
0000     32 bit integer  0x00000803(2051) magic number 
0004     32 bit integer  10000            number of images 
0008     32 bit integer  28               number of rows 
0012     32 bit integer  28               number of columns 
0016     unsigned byte   ??               pixel 
0017     unsigned byte   ??               pixel 
........ 
xxxx     unsigned byte   ??               pixel


Please note that your browser may uncompress these files without telling you.
If the files you downloaded have a larger size than the above, they have been uncompressed by your browser. Simply rename them to remove the .gz extension. Some people have asked me "my application can't open your image files". These files are not in any standard image format. You have to write your own (very simple) program to read them. The file format is described at the bottom of this page.

