# PySnake
Author: sxntrxn

## To install the dependencies for this project, follow these steps:

1. Create a virtual environment by running the following command in your terminal:
  ```
  python -m venv .venv
  ```

2. Activate the virtual environment. Depending on your operating system, use one of the following commands:
  - For Windows:
    ```
    .venv\Scripts\activate.bat
    ```
  - For macOS/Linux:
    ```
    source .venv/bin/activate
    ```

3. Once the virtual environment is activated, install the dependencies from the `requirements.txt` file by running the following command:
  ```
  pip install -r requirements.txt
  ```

4. Wait for the installation process to complete. This will install all the required dependencies for the project.

You have now successfully installed the dependencies for the project. You can proceed with running the application or executing any other necessary steps.

## To run the game, follow these steps:
1. Run the game by executing the `main.py` file:
  ```
  python main.py
  ```

2. The console will prompt you to enter the size of the board. Provide the desired size and press Enter.

3. The game will create the board and you can start playing by pressing the spacebar.

4. To pause the game, press the spacebar again. You can restart the game by pressing space when you lose or win.

## Special Configurations
### Changing the game speed
You can change the speed of the game by modifying the `TICK_RATE` variable in the `main.py` file.
The `TICK_RATE` variable determines the number of times the game updates per second. By default, it is set to `1`.

This value is planned to be configurable in-game in future updates. For now, you can manually change it in the code.