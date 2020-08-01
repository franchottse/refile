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

-   Users can add multiple ~~Excel~~ files 🙎‍♂️🙎‍♀️🗂
-   Users can view different files by selecting files 🙎‍♂️🙎‍♀️🗃
-   Users can view selected columns only 🙎‍♂️🙎‍♀️📋
-   Users can edit data within the app 🙎‍♂️🙎‍♀️📝

<!-- '![example-app](example-app.gif)' need removing the quotes -->

<!-- OBJECTIVES -->

<a name="objectives" />

## Objectives

-   [ ] 🎨 Create the GUI
-   [ ] 📝 Create two fields for <del>columns, </del>contents and files
-   [ ] 📑 Let user add files to the file field
-   [ ] 📖 Compare the differences in two files
-   [ ] 🗃 Save the added file names for the next time use
-   [ ] 🙈 Show/Hide text difference
-   [ ] 📋 Show a pop-up window for output data
-   [ ] 💾 Save the output data to <del>existing or </del>new ~~Excel~~ Word, PDF or text files
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
-   [ ] Create option frame
    -   [ ] Options and checkboxes
        -   [ ] Underline
        -   [ ] Strikethrough
        -   [ ] Highlight
        -   [ ] Left text box
        -   [ ] Right text box
        -   [ ] Change highlight words style only
        -   [ ] Show/Hide ¶
    -   [ ] scrollbar
-   [ ] Create content frame
    -   [x] Scrollbar
    -   [x] Two text boxes
    -   [ ] Pop-up window when clicking merge files button the data
        -   [ ] Text box
        -   [ ] Label
        -   [ ] Buttons
            -   [ ] Save Output
            -   [ ] Cancel
    -   [ ] Lines highlighting if possible
-   [x] Create file frame
    -   [x] A scrollbar
    -   [x] File icon and name
    -   [x] Files Deletion
    -   [x] Double-click to open file function
    -   [x] File name wrapper
-   [x] Create button frame
    -   [x] Open File
    -   [ ] Merge (Diff) Text
    -   [ ] Clear Contents (may add)
    -   [x] Clear All Files
-   [ ] Create right click menu
    -   [ ] Delete file
    -   [ ] Properties
-   [ ] Create menu bar
    -   [ ] File
        -   [ ] Open files
        -   [ ] Exit
    -   [ ] Font
    -   [ ] About
-   [x] Create status bar frame

<a name="back-end" />

### Back-end

-   [ ] Make sure the files can be read
-   [ ] Fetch data from Word, text or PDF files
-   [ ] Read text from Word, text or PDF files
-   [ ] Put text to the GUI
-   [ ] Show the differences from two files
-   [ ] Display the output on a pop-up window
-   [ ] Bind two functions: "Save Output" for saving output text
-   [ ] Bind functions for deleting one or all files

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
