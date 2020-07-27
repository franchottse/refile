<!-- PROJECT TITLE -->

# ReFile - Excel file reader

A basic Excel file reader to show and edit data which is in the form of table with Tkinter GUI.

<!-- TABLE OF CONTENTS -->

## Table of Contents

- [Motivation](#motivation)
- [Feature](#feature)
- [Objectives](#objectives)
- [Installation](#installation)
- [Task List](#task-list)
  - [GUI](#gui)
  - [Back-end](#back-end)
  - [Convertion](#convertion)
- [License](#license)

<!-- MOTIVATION -->

<a name="motivation" />

## Motivation

The reason for creating this Python app is for my friends, they work at a company which involves lots of Excel files, and they hope they could have something app like this. For example, they want to view some rows that do not contain some of the data, like phone number or address.

<!-- FEATURE -->

<a name="feature" />

## Feature

With the following features:

- Users can add multiple Excel files 🙎‍♂️🙎‍♀️🗂
- Users can view different files by selecting files 🙎‍♂️🙎‍♀️🗃
- Users can view selected columns only 🙎‍♂️🙎‍♀️📋
- Users can edit data within the app 🙎‍♂️🙎‍♀️📝

<!-- '![example-app](example-app.gif)' need removing the quotes -->

<!-- OBJECTIVES -->

<a name="objectives" />

## Objectives

- [ ] 🎨 Create the GUI
- [ ] 📝 Create three fields for columns, data and files
- [ ] 📑 Let user add files to the file field
- [ ] 📖 Read the columns from the file and display them in columns field
- [ ] 🗃 Save the added file names for the next time use
- [ ] 🙈 Show/Hide selected columns data
- [ ] 📋 Show a pop-up window for editing the data (row)
- [ ] 💾 Save the edited data to existing or new Excel files
- [ ] 🚀 Convert the whole app into an installable or a .EXE file

<!-- INSTALLATION -->

<a name="installation" />

## Installation

The repo contains two executable files, one is installable, another one is of .EXE. You can download either one to use the app.

<!-- TASK LIST -->

<a name="task-list" />

## Task List

<a name="gui" />

### GUI

- [x] Create the main window
- [ ] Create column frame
  - [ ] Column names and checkboxes
  - [ ] A scrollbar
- [ ] Create data frame
  - [x] Treeview
  - [x] Two scrollbars
  - [ ] Pop-up window when double clicking the data (row)
  - [ ] Add row button
  - [ ] Delete row button
- [ ] Create file frame
  - [x] A scrollbar
  - [x] File icon and name
  - [x] Files Deletion
  - [ ] Double-click to open file function
- [x] Create button frame
  - [x] Open File
  - [x] Clear All File
- [ ] Create right click menu
  - [ ] Delete file
- [ ] Create menu bar
  - [ ] File
  - [ ] About
- [x] Create status bar frame

<a name="back-end" />

### Back-end

- [ ] Make sure the files can be read
- [ ] Fetch data from Excel files
- [ ] Read colums, sheets from Excel files
- [ ] Put colums, sheets and data to the GUI
- [ ] Bind two functions: "Save" and "Save As" for saving edited data
- [ ] Bind functions for deleting one, a few or all files
- [ ] Bind a function when deleting files for unsaved files
- [ ] Bind a function when closing window for unsaved data
- [ ] Bind a function with adding and deleting rows

<a name="convertion" />

### Convertion

- [ ] Convert whole app into one installable file
- [ ] Convert whole app into a .EXE file

<a name="license" />

## License

Distributed under the MIT License. See `LICENSE` for more information.

MIT © [Frankie Tse]()
