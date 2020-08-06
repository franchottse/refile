<!-- PROJECT TITLE -->

# ReFile - Excel file reader

A basic text file reader to show contents and see differences with Tkinter GUI.

<!-- TABLE OF CONTENTS -->

## Table of Contents

-   [Motivation](#motivation)
-   [Feature](#feature)
-   [Objectives](#objectives)
-   [Installation](#installation)
-   [Task List](#task-list)
    -   [GUI](#gui)
    -   [Back-end](#back-end)
    -   [Convertion](#convertion)
-   [License](#license)

<!-- MOTIVATION -->

<a name="motivation" />

## Motivation

The reason for creating this Python app is for my friends, they work at a company which involves lots of text files, and they hope they could have something app to compare and output the differences. For example, the words "Hello World" and "Hi World" will output as "Hi Hello World" and highlight "Hi" and "Hello" to tell the difference.

<!-- FEATURE -->

<a name="feature" />

## Feature

With the following features:

-   Users can add multiple files 🙎‍♂️🙎‍♀️🗂
-   Users can view different files by selecting files 🙎‍♂️🙎‍♀️🗃
-   Users can enable/disable differences from two selected files 🙎‍♂️🙎‍♀️📋

<!-- '![example-app](example-app.gif)' need removing the quotes -->

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
-   [ ] 💾 Save the output data to new Word, PDF ~~or text~~ files
-   [ ] 🚀 Convert the whole app into an installable or a .EXE file

<!-- INSTALLATION -->

<a name="installation" />

## Installation

The repo contains two executable files, one is installable, another one is of .EXE. You can download either one to use this app.

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
-   [ ] Create content frame
    -   [ ] Scrollbars
    -   [x] Two text boxes
    -   [ ] Pop-up window when clicking merge files button the data
        -   [ ] Text box scrollbar frame
            -   [x] Text box
            -   [ ] Scrollbars
        -   [ ] Merge text result and button frame
            -   [x] Result label
            -   [x] Buttons
                -   [ ] Save Output
                -   [x] Cancel
-   [x] Create file frame
    -   [x] A scrollbar
    -   [x] File icon and name
    -   [x] Files Deletion
    -   [x] Double-click to open file function
    -   [x] File name wrapper
-   [x] Create button frame
    -   [x] ~~Open File~~
    -   [ ] Merge (Diff) Text
    -   [x] Clear Contents
    -   [x] ~~Clear All Files~~
-   [ ] Create right click menu
    -   [ ] Delete file
    -   [ ] Properties
-   [ ] Create menu bar
    -   [ ] File
        -   [x] Open
        -   [x] Clear All
        -   [x] Exit
    -   [ ] Format
        -   [x] Word Wrap
        -   [x] Font Size
        -   [x] Clear Style
    -   [ ] Help
        -   [x] How to use
        -   [x] About ReFile
-   [x] Create status bar frame

<a name="back-end" />

### Back-end

-   [x] Make sure the files can be read
-   [x] Fetch data from Word, text or PDF files
-   [x] Read text from Word, text or PDF files
-   [ ] Put text to the GUI
-   [ ] Show the differences from two files
-   [ ] Display the output on a pop-up window
-   [ ] Bind functions for all four options
-   [ ] Bind two functions: "Save Output" for saving output text
-   [ ] Bind functions for deleting one or all files
-   [ ] Bind functions to all menu options

<a name="convertion" />

### Convertion

-   [ ] Convert whole app into one installable file
-   [ ] Convert whole app into a .EXE file

<!-- LICENSE -->

<a name="license" />

## License

Distributed under the MIT License. See `LICENSE` for more information.

MIT © [Frankie Tse]()

<!-- ATTRIBUTION -->

<a name="attribution" />

## Attribution

-   "[Docs, google, word icon](https://www.iconfinder.com/icons/97957/docs_google_word_icon)" by [Dakirby309](https://www.deviantart.com/dakirby309), used under [CC BY](https://creativecommons.org/licenses/by-nc/3.0/) / Resized from original
-   "[Documents icon](https://www.iconfinder.com/icons/99038/documents_icon)" by [Dakirby309](https://www.deviantart.com/dakirby309)
-   "[Acrobat, adobe, reader icon](https://www.iconfinder.com/icons/99074/acrobat_adobe_reader_icon)" by [Dakirby309](https://www.deviantart.com/dakirby309)
-   "[Button PNG](http://pngimg.com/download/31565)" by [pngimg.com](http://pngimg.com/), used under [CC BY](https://creativecommons.org/licenses/by-nc/4.0/) / Resized from original
-   [Toggle On icon](https://icons8.com/icons/set/toggle-on) icon by [Icons8](https://icons8.com)
-   [Toggle Off icon](https://icons8.com/icons/set/toggle-off) icon by [Icons8](https://icons8.com)
-   [Unchecked Radio Button icon](https://icons8.com/icons/set/unchecked-radio-button) icon by [Icons8](https://icons8.com)
-   [Checked Radio Button icon](https://icons8.com/icons/set/checked-radio-button) icon by [Icons8](https://icons8.com)
-   [Compare icon](https://icons8.com/icons/set/compare) icon by [Icons8](https://icons8.com)
