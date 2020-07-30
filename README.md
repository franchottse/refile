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
-   [ ] Create ~~column~~ option frame (may remove that later on)
    -   [ ] Options and checkboxes
        -   [ ] Bold
        -   [ ] Italic
        -   [ ] Underline
        -   [ ] Highlight
    -   [ ] A scrollbar
-   [ ] Create ~~data~~ contents frame
    -   [x] ~~Treeview~~
    -   [x] Two scrollbars
    -   [ ] Two text boxes
    -   [ ] Pop-up window when clicking merge files button the data
    -   [ ] Lines highlighting if possible
    -   [ ] ~~Add row button~~
    -   [ ] ~~Delete row button~~
-   [x] Create file frame
    -   [x] A scrollbar
    -   [x] File icon and name
    -   [x] Files Deletion
    -   [x] Double-click to open file function
    -   [x] File name wrapper
-   [x] Create button frame
    -   [x] Open File
    -   [ ] Merge (or Compare) Files
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
-   [ ] Fetch data from ~~Excel~~ Word, PDF or text files
-   [ ] Read ~~colums, sheets~~ texts from ~~Excel~~ Word, PDF or text files
-   [ ] Put ~~colums, sheets~~ texts and data to the GUI
-   [ ] Spot the differences in two files
-   [ ] Display the output on a pop-up window
-   [ ] Bind two functions: "Save" and "Save As" for saving output data
-   [ ] Bind functions for deleting one~~, a few~~ or all files
-   [ ] ~~Bind a function when deleting files for unsaved files~~
-   [ ] ~~Bind a function when closing window for unsaved data~~
-   [ ] ~~Bind a function with adding and deleting rows~~

<a name="convertion" />

### Convertion

-   [ ] Convert whole app into one installable file
-   [ ] Convert whole app into a .EXE file

<a name="license" />

## License

Distributed under the MIT License. See `LICENSE` for more information.

MIT © [Frankie Tse]()
