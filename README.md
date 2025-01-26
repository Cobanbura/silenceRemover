
# Silence Remover

Silence Remover will be your assistant for removing the silent moments of your voice or video records to make things easier for you.

## Features

- Python and `moviepy`, `pydub`, and `os` libraries are implemented and used to remove silent moments from audio or video files.
- Customizable padding and threshold values allow users to fine-tune the silence removal experience.

## Installation

### Prerequisites

- Python 3.x (make sure Python 3.6 or later is installed)

You can install the required libraries by running the following command:

```bash
pip install -r requirements.txt
```

Here are the libraries included in `requirements.txt`:

- `moviepy` (for video editing and processing)
- `pydub` (for audio manipulation and silence detection)
- `os` (for file handling)

These libraries will handle the processing of audio/video files and silence detection/removal.

### Clone the Repository

To get started, clone this repository:

```bash
git clone https://github.com/yourusername/silence-remover.git
cd silence-remover
```

## Usage

To run the project and remove silence from an audio or video file, use the following command:

```bash
python silence_remover.py input_file output_file
```

Make sure to replace `input_file` with the path to your input file (audio/video) and `output_file` with the desired output path.

### How the Program Works

The program checks for files in the following data folder:

```python
data_folder = '../data'
```

It will process each file found in the `data_folder` and remove silence based on the padding and threshold configuration you set.

### Configuration

You can adjust the following parameters to customize your experience:

- `padding`: Controls the length of the silence before and after detected silence that will be removed. Modify this value to fine-tune how much silence is trimmed.
- `threshold`: Defines the volume threshold to detect silence. A higher threshold might help filter out quieter parts, while a lower one might detect softer sounds as silence.

## Contributing

I (the author) have written the initial version of this code, but any contributions to further improve or expand the project are welcome! Feel free to submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Currently, there is no direct contact for this project. Feel free to contribute or open issues via GitHub if you encounter any problems or have suggestions.
