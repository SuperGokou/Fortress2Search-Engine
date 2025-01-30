# Fortress 2 Item Search Engine

## Team Members
- Ming Xia
- Jack Knudson

## Features

### User Interface
- **Autocomplete**: Provides real-time search recommendations as the user types.
- **No Results Page**: Displays a user-friendly page when no relevant items are found.
- **Images**: Thumbnails from Steam are displayed next to each item for better recognition.
- **Results Formatting**: Search results are split into multiple pages, with ten items per page.
- **External Links**: Each item includes a link to the Steam profile it was found on, or a default notification page if the link is inactive.

### Search Functionality
- **Advanced Search**: Allows users to refine searches by item characteristics such as quality or class.
- **Statistical Figures**: Generates statistics showing the number of similar items or class statistics.
- **Word Filtering**: Filters out common but irrelevant words from the search queries.

## Technologies

- **Whoosh**: Utilized for searching and ranking information within the dataset.
- **BM25**: Employs the BM25 algorithm for querying the dataset to find the most relevant items.
- **PySQLite**: Manages the dataset storage using an SQLite database.

## Dataset Description

The dataset comprises custom-named items from "Team Fortress 2". Each record includes:
- **Original Name**: The default name of the item.
- **Usage**: Which characters can use the item in-game.
- **Quality**: Attributes that may affect the item's properties.
- **Description**: Includes player-custom descriptions or achievements associated with the item.
- **Owner Information**: Links to the owner's Steam profile.
- **Thumbnail Image**: Visual representation of the item.


