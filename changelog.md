# RaspCloud changelog

\[v0.2.1 (BETA)]
#### Additions
```text
- [FRONTEND] Add error page
- [FRONTEND] Add coming soon to ACP and Settings
```

\[v0.2 (BETA)]

#### Additions
```text
- [FRONTEND] Add logout option under avatar menu in navbar
- [FRONTEND] Add (expected) file size to add file modal when file is selected
- [FRONTEND] Add progress bar under file upload
- [FRONTEND] Added functionality to the ellipsis besides files and folders
- [FRONTEND] Added ability to delete files and folders
- [FRONTEND] Added ability to rename files and folders
```

#### Changes
```text
- [FRONTEND] Changed upload file from a "fetch" javascript function to an XHR
- Encapsulated folder paths in URI under the "files/" path to prevent name shadowing, resulting in unaccessable folders or routes.
- Add function to replace spaces in file and folder names with '_'
- [FRONTEND] Improved mobile responsiveness
- Removed autocomplete from inputs
```

#### Bug Fixes
```text
- Make all "/dl" routes require login.
- [FRONTEND] Removing files from upload queue works now.
- Add error checks in "bytes_to_human" function of dh.py
- [FRONTEND] Fixed wrong url
```

\[v0.1 (BETA)]
```text
- First version!
```
