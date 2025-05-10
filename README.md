# LibraryFace

LibraryFace is a Python-based application designed to manage and process datasets related to anime, movies, and TV shows. It provides utilities for handling icons, searching metadata, and managing layouts for user interfaces.

## Features

- **Dataset Management**: Includes tools to clean and process datasets for anime, movies, and TV shows.
- **Icon Utilities**: Convert, fetch, and manage icons for various media.
- **Metadata Search**: Search and normalize metadata using APIs like Jikan, OMDB, and TMDB.
- **UI Layouts**: Predefined layouts for application settings, popups, and match layouts.
- **Undo Utilities**: Tools to undo changes made to icons and posters.
- **Handlers**: General and specific handlers for managing application workflows.

## Project Structure

- **assets/**: Contains datasets and media assets like icons and images.
- **build/**: Generated files and packages for the application.
- **core/**: Core configuration and assets for the application.
- **hooks/**: Custom hooks for integrating with external libraries.
- **logic/**: Core logic for handling tasks, utilities, and metadata.
- **ui/**: User interface components and layouts.
- **handlers/**: Handlers for managing workflows and options.
- **helpers/**: Helper scripts for expanding, logging, and managing paths.

## Getting Started

1. Clone the repository:
   ```powershell
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```powershell
   cd LibraryFace
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Run the application:
   ```powershell
   python main.py
   ```

## Requirements

- Python 3.10 or higher
- Required Python libraries (listed in `requirements.txt`)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [Jikan API](https://jikan.moe/) for anime metadata.
- [OMDB API](https://www.omdbapi.com/) for movie metadata.
- [TMDB API](https://www.themoviedb.org/) for TV show metadata.
