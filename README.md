

```markdown
# Euro 2024 Shot Analysis

This project is a Streamlit web application that allows users to analyze shot data from the Euro 2024 tournament. Users can select matches and view detailed shot visualizations, including player locations, shot outcomes, and expected goals (xG).

## Features

- **Match Selection**: Choose from a list of Euro 2024 matches to analyze.
- **Shot Visualization**: View detailed visualizations of shots taken during the selected match, including the shooter and other players' positions.
- **Team Shot Statistics**: Display a table of total shots taken by each team in the match.
- **Shot Details**: Information on each shot including time, team, player, outcome, and expected goals (xG).
- **Goal Visualization**: If applicable, visualize the shot's end location in relation to the goal.

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly Express
- StatsBombPy
- MPLsoccer
- Matplotlib
- PIL (Pillow)

## Installation

To run this application locally, you need to have Python installed. You can then create a virtual environment and install the required packages:

```bash
# Clone the repository
git clone <repository-url>
cd <repository-directory>

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the required packages
pip install streamlit pandas plotly statsbombpy mplsoccer matplotlib pillow
```

## Usage

After installing the required packages, you can run the application using the following command:

```bash
streamlit run app.py
```

Open your web browser and navigate to `http://localhost:8501` to view the application.

## Data Source

This application uses the StatsBomb data API to fetch match and shot data for Euro 2024. Ensure you have the necessary access to use this data.

## Contributing

Contributions are welcome! If you have suggestions for improvements or features, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

### Instructions:
- Replace `<repository-url>` with the actual URL of your GitHub repository.
- Replace `<repository-directory>` with the name of your repository directory.
- If you have a license file, ensure it is in the same directory as the README and adjust the license section accordingly.

You can copy and paste this directly into your `README.md` file in your GitHub repository. Let me know if you need any changes or additional information!
