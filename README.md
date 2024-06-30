```markdown
# Brute Force Login Tool

This project is a brute force login tool that attempts to log in to a target website using a list of usernames and passwords. It has both automatic and manual modes to extract and use form fields for login attempts.

## Features

- **Automatic Mode**: Automatically extracts form fields from the target login page.
- **Manual Mode**: Allows the user to manually input form field names.
- **Logging**: Logs all activities and results to a log file.
- **Result Saving**: Saves successful login attempts to a results file.

## Requirements

- Python 3.x
- `requests` library

## Installation

1. Clone the repository:
   ```python
   git clone https://github.com/d1v45/Brute-Force-Tool.git
   cd Brute-Force-Tool
   ```

2. Install the required libraries:
   ```python
   pip install requests
   ```

## Usage

1. Open the bruteit.py file to include your list of usernames (`USERS`) and passwords (`PASSWORDS`). You should also set the limit for trying to access the URL (`LIMIT_TRYING_ACCESSING_URL`) and the incorrect and success messages (`INCORRECT_MESSAGE`, `SUCCESS_MESSAGE`).

2. Run the `bruteit.py` script:
   ```python
   python3 bruteit.py
   ```

3. Follow the prompts to select the mode and provide necessary information.

### Manual Mode

In manual mode, you will need to provide the following details:
- Target URL (the `action` attribute of the form tag)
- User Field (the `name` attribute of the login form for the username/email)
- Password Field (the `name` attribute of the login form for the password)
- CSRF Token Field (optional, the `name` attribute of the login form for the CSRF token)

### Automatic Mode

In automatic mode, you only need to provide the target URL. The script will attempt to extract form fields automatically.

## Logging and Results

- Logs are saved in `bruteforce.log`.
- Successful login attempts are saved in `results.txt`.

## Disclaimer

This tool is for educational purposes only. Unauthorized use of this tool is illegal and unethical. The author is not responsible for any misuse of this tool.

## Author

- DIVAS

## License

This project is licensed under the MIT License.
```
