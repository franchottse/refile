<!-- PROJECT TITLE -->

# ReFile - Excel file reader

A basic text file reader to show contents and see differences with Tkinter GUI.

<!-- TABLE OF CONTENTS -->

## Table of Contents

-   [Motivation](#motivation)
-   [Feature](#feature)
-   [Objectives](#objectives)
-   [How To Use](#how-to-use)
-   [Installation](#installation)
-   [Task List](#task-list)
    -   [GUI](#gui)
    -   [Back-end](#back-end)
    -   [Convertion](#convertion)
-   [License](#license)

<!-- MOTIVATION -->

<a name="motivation" />

## Motivation

The reason for creating this Python app is for my friends, they work at a company which involves lots of text files, and they hope they could have something app to compare and output the differences. For example, the words **"Hello World"** and **"Hi World"** will output as "**H<del style="background-color: #FFAAAA">ello</del><ins style="background-color: #AAFFAA">i</ins> World**" and highlight the difference.

<!-- FEATURE -->

<a name="feature" />

## Feature

With the following features:

-   Users can add multiple files 🙎‍♂️🙎‍♀️🗂
-   Users can view different files by selecting files 🙎‍♂️🙎‍♀️🗃
-   Users can enable/disable differences from two selected files 🙎‍♂️🙎‍♀️📋

![example-app](example-app.gif "ReFile example")

<!-- OBJECTIVES -->

<a name="objectives" />

## Objectives

-   [ ] 🎨 Create the GUI
-   [ ] 📝 Create two fields for contents and files
-   [ ] 📑 Let user add files to the file field
-   [ ] 📖 Compare the differences in two files
-   [ ] 🗃 Save the added files for the next time use
-   [ ] 🙈 Show/Hide text difference
-   [ ] 📋 Show a pop-up window for output data
-   [ ] 💾 Save the output data to new Word or PDF files
-   [ ] 🚀 Convert the whole app into an installable or a .EXE file

<!-- INSTALLATION -->

<a name="installation" />

## Installation

The repo contains an executable file, which is an installer. A standalone .EXE file may be added later on so that you can download either one to use this app.

<!-- HOW TO USE -->

<a name="how-to-use" />

## How To Use

-   **Select File**: press `Ctrl+O` or Double click in file field
-   **Delete all file in file field**: `Ctrl+D`
-   **Merge Text**: press `Ctrl+M`
-   **Change Text Box**: Click the `Options` on the left or the text box itself
-   **Open File**: press `Ctrl+Enter` when focusing a file or use right click menu
-   **Copy Text**: press `Ctrl+C` when focusing a file or use right click menu
-   **Copy Path**: press `Shift+Alt+C` when focusing a file or use right click menu
-   **Copy Relative Path**: press `Ctrl+Shift+C` when focusing a file or use right click menu
-   **Delete a File**: press `Del` when focusing a file or use right click menu

<!-- TASK LIST -->

<a name="task-list" />

## Task List

<a name="gui" />

### GUI

-   [x] Create the main window
-   [x] Create option frame
    -   [x] Options and checkboxes
        -   [x] Text Box
            -   [x] Left Text Box
            -   [x] Right Text Box
        -   [x] Style
            -   [x] Underline Insertion
            -   [x] Strikethrough Deletion
            -   [x] Highlight Insertion/Deletion
            -   [x] Show/Hide ¶
-   [x] Create content frame
    -   [x] Scrollbars
    -   [x] Two text boxes
    -   [x] Pop-up window when clicking merge files button the data
        -   [x] Text box scrollbar frame
            -   [x] Text box
            -   [x] Scrollbars
        -   [x] Merge text result and button frame
            -   [x] Result label
            -   [x] Buttons
                -   [x] Save Output
                -   [x] Cancel
-   [x] Create file frame
    -   [x] A scrollbar
    -   [x] File icon and name
    -   [x] Files Deletion
    -   [x] Double-click to open file function
    -   [x] File name wrapper
-   [x] Create button frame
    -   [x] Merge Text
    -   [x] Clear Contents
-   [x] Create right click menu
    -   [x] Open
    -   [x] Copy Text
    -   [x] Copy Path
    -   [x] Copy Relative Path
    -   [x] Delete
-   [x] Create menu bar
    -   [x] File
        -   [x] Open
        -   [x] Clear All
        -   [x] Merge Text
        -   [x] Exit
    -   [x] Format
        -   [x] Word Wrap
        -   [x] Font Size
        -   [x] Clear Style
    -   [x] Help
        -   [x] How to use
        -   [x] Release notes
        -   [x] About ReFile
-   [x] Create status bar frame
-   [x] Create tooltips
    -   [x] Left Text Box
    -   [x] Right Text Box
    -   [x] Files
    -   [x] Merge Text button
    -   [x] Clear Contents button

<a name="back-end" />

### Back-end

-   [x] Make sure the files can be read
-   [x] Fetch data from Word, text or PDF files
-   [x] Read text from Word, text or PDF files
-   [x] Put text to the GUI
-   [x] Show the differences from two files
-   [x] Display the output on a pop-up window
-   [x] Bind functions to all four options
-   [x] Bind function to "Save Output" for saving output text
-   [x] Bind functions to deleting one or all files
-   [x] Bind functions to all menu options
-   [x] Save file names and settings when closing app

<a name="convertion" />

### Convertion

-   [x] Convert whole app into one installable file
-   [ ] Convert whole app into a standalone .EXE file

<!-- LICENSE -->

<a name="license" />

## License

Distributed under the MIT License. See `LICENSE` for more information.

MIT © [Frankie Tse](https://github.com/franchottse)

<!-- ATTRIBUTION -->

<a name="attribution" />

## Attribution

-   "[Docs, google, word icon](https://www.iconfinder.com/icons/97957/docs_google_word_icon)" by [Dakirby309](https://www.deviantart.com/dakirby309), used under [CC BY](https://creativecommons.org/licenses/by-nc/3.0/) / Resized from original
-   "[Documents icon](https://www.iconfinder.com/icons/99038/documents_icon)" by [Dakirby309](https://www.deviantart.com/dakirby309)
-   "[Acrobat, adobe, reader icon](https://www.iconfinder.com/icons/99074/acrobat_adobe_reader_icon)" by [Dakirby309](https://www.deviantart.com/dakirby309)
-   [Toggle On icon](https://icons8.com/icons/set/toggle-on) icon by [Icons8](https://icons8.com)
-   [Toggle Off icon](https://icons8.com/icons/set/toggle-off) icon by [Icons8](https://icons8.com)
-   [Unchecked Radio Button icon](https://icons8.com/icons/set/unchecked-radio-button) icon by [Icons8](https://icons8.com)
-   [Checked Radio Button icon](https://icons8.com/icons/set/checked-radio-button) icon by [Icons8](https://icons8.com)
-   [Compare icon](https://icons8.com/icons/set/compare) icon by [Icons8](https://icons8.com)
