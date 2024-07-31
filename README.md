### README.md

---

# CS:GO Bot Project

## Overview
This project involves the development of an assistant application for the game Counter-Strike: Global Offensive (CS:GO) (and may be suitable for CS2) utilizing neural networks for object detection and an algorithm for smooth aim movement.

## Technologies Used
- **Python**: Main programming language.
- **YOLOv8**: For object detection.
- **WindMouse**: For smooth mouse movements.
- **OpenCV**: For image processing.
- **Visual Studio Code**: Development environment.
- **Git**: Version control.

## Project Structure
- **Data Preparation**: Collecting and annotating images for training the YOLOv8 model.
- **Model Training**: Training the YOLOv8 model using the prepared dataset.
- **Application Development**: Integrating the trained model with a real-time application to detect and assist in aiming at game characters.
- **Testing and Evaluation**: Evaluating the model's performance and making necessary improvements.

## Features
- **Real-time Object Detection**: Detects game characters (both body and head of Counter-Terrorists and Terrorists) in real-time using the YOLOv8 model.
- **Smooth Aiming**: Uses the WindMouse algorithm to move the aim smoothly towards detected targets.
- **High Accuracy**: The model achieves over 80% accuracy in detecting characters.
- **Fast Reaction Time**: The application reacts within 0.050 seconds to ensure smooth gameplay.

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/Kolyanuss/csgo_bot.git
    ```
2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```
3. Download [Model](https://drive.google.com/file/d/1_ib6hcfsywX4I_qj-mdiBvJfNbHVgGP4/view?usp=sharing)
 file and place inside `config_files` folder.

## Usage
Start `RUN.bat`
- `Home` key -> activate detecting script
- `End` key -> deactivate detecting (to conserve resources)
- `Left Shift` key (with activated detecting) -> start AIM and fire mode
- `Left Alt` key -> stop AIM and fire
- `DEL` key -> exit program

## Results
- The application processes an average of 41 frames per second.
- Demonstrated detection accuracy of 90% for player heads and bodies.

## Acknowledgements
This project was developed as a part of a diploma work at the Chernivtsi National University under the supervision of assistant V. V. Dvorzhak.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
