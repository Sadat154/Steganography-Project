# Image Steganography Project

A Python-based image steganography project implementing and comparing two methods of hiding textual information inside digital images:

* **Bit Substitution**
* **Discrete Cosine Transform (DCT) Steganography**

The project was originally developed as my Computer Science NEA and focuses on how different embedding methods, bit positions, payload sizes and colour channels affect the resulting image.

## Overview

Steganography is the process of hiding information within another medium so that the existence of the hidden information is not immediately apparent.

This project explores image steganography by converting text into binary data and embedding it inside an image. It implements both a spatial-domain technique and a frequency-domain technique, allowing the two approaches to be compared.

The program can encode and decode hidden messages, automatically generate experimental output images and produce an HTML page for visually comparing the results.

## Key Features

* Encode text messages inside digital images
* Decode previously embedded messages
* Two independent steganography algorithms
* Testing across all 8 bit positions
* DCT embedding across red, green and blue colour channels
* Automatic testing at 25%, 50%, 75% and 100% of available capacity
* Support for user-supplied images
* Validation of image formats and message capacity
* Automated generation of comparison images
* HTML results page for viewing experimental outputs
* Unit and functional testing

## Algorithms

### 1. Bit Substitution

The bit-substitution algorithm works directly with image pixel values.

RGB images consist of red, green and blue channel values, each represented using 8 bits. The secret message is converted into binary and individual message bits are substituted into a selected bit position of these pixel values.

For example:

```text
Original value: 10011001
Message bit:    0
Modified value: 10011000
```

Changing less significant bits causes relatively small changes to the original pixel value, while altering more significant bits can introduce greater visible distortion.

Rather than limiting the experiment to the Least Significant Bit, the program tests all **8 possible bit positions**. This allows the effect of bit significance on image quality to be observed.

The decoding process reverses this operation by extracting the selected bits and reconstructing the original text.

### 2. DCT Steganography

The second technique uses the **Discrete Cosine Transform**.

Instead of directly modifying pixel values, the program divides a selected image colour channel into **8 × 8 blocks** and transforms these blocks into the frequency domain.

The general process is:

```text
Input Image
    ↓
Select RGB Channel
    ↓
Divide into 8 × 8 Blocks
    ↓
Apply DCT
    ↓
Quantise Coefficients
    ↓
Embed Message
    ↓
Reconstruct Image
```

The implementation uses OpenCV for DCT operations and NumPy for numerical processing.

The program can independently embed information into the:

* Red channel
* Green channel
* Blue channel

This allows the effect of modifying different colour channels to be compared.

## Experimental Approach

The program was designed to test the algorithms systematically rather than demonstrate only a single successful encoding.

For bit substitution, each image can be tested using:

* 8 bit positions
* 4 payload sizes

The payload levels are:

```text
25%
50%
75%
100%
```

This produces up to **32 experimental images per source image**.

For DCT steganography, the program additionally tests all three RGB channels:

```text
8 bit positions
× 4 payload levels
× 3 colour channels
```

This produces up to **96 experimental images per source image**.

The purpose of these experiments is to observe how factors such as message size, bit significance and colour-channel selection affect the appearance of the final image.

## Project Structure

```text
Steganography-Project/
│
├── Algorithms/
│   ├── BitSubStega.py
│   ├── DCTStega.py
│   ├── SteganographyAlgorithm.py
│   ├── Main.py
│   ├── Testing.py
│   └── Unittest.py
│
├── DefaultImages/
├── UserImages/
│
├── ModifiedImages/
│   ├── BitSubModifiedImages/
│   └── DCTModifiedImages/
│
├── Prototype/
├── INSTRUCTIONS.txt
└── README.md
```

### Main Components

**`Main.py`**

Controls the application, handles user input, validates images, executes experiments and generates the HTML results page.

**`BitSubStega.py`**

Contains the bit-substitution encoder and decoder.

**`DCTStega.py`**

Contains the DCT-based encoding and decoding implementation.

**`SteganographyAlgorithm.py`**

A shared base class containing reusable functions used by both algorithms.

**`Testing.py` and `Unittest.py`**

Contain functional and unit tests used to verify the implementation.

## Technologies

The project primarily uses:

* **Python**
* **Pillow** for image processing
* **NumPy** for numerical operations
* **OpenCV** for DCT transformations
* **HTML/CSS** for displaying experimental results
* **Python unittest** for testing

## Installation

Clone the repository:

```bash
git clone https://github.com/Sadat154/Steganography-Project.git
cd Steganography-Project
```

Install the required dependencies:

```bash
pip install pillow numpy opencv-python
```

## Running the Program

Navigate to the algorithm directory:

```bash
cd Algorithms
```

Run:

```bash
python Main.py
```

The program will ask which algorithm you would like to test:

```text
1. Bit Substitution Based Steganography
2. DCT Based Steganography
3. Both
```

You can then choose between the included default images or your own images.

## Using Your Own Images

Place images inside:

```text
UserImages/
```

Supported formats include:

```text
JPG
JPEG
PNG
BMP
WEBP
```

The program validates the image before processing it and prevents messages from being encoded when they exceed the available image capacity.

## Results

Generated images are stored under:

```text
ModifiedImages/
```

with separate directories for the two algorithms.

After processing, the program automatically generates an:

```text
Index.html
```

page containing the experimental images.

This makes it possible to visually compare the effects of:

* different bit positions
* different message sizes
* different colour channels
* different steganography techniques

without manually opening every generated image.

## Testing

The project includes both functional and unit testing.

Tests cover areas including:

* normal message encoding
* message decoding
* maximum-capacity messages
* messages exceeding image capacity
* different bit positions
* different DCT colour channels
* reusable helper functions

A message can therefore be encoded into an image, decoded again and compared with the original value to verify that the complete process works correctly.

## Design

The project follows an object-oriented structure.

Both algorithms inherit shared functionality from a common `SteganographyAlgorithm` base class.

```text
             SteganographyAlgorithm
                     │
             ┌───────┴───────┐
             │               │
             ▼               ▼
BitSubEncoderDecoder      DCTSteg
```

This reduces duplicated code and makes it easier to extend the project with additional steganography methods.

## Author

**Sadat Nafis**

GitHub: `Sadat154`
