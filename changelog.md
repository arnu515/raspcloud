# RaspCloud changelog

\[v0.2 (BETA)]

#### Additions
```text
- [FRONTEND] Add logout option under avatar menu in navbar
- [FRONTEND] Add (expected) file size to add file modal when file is selected
- [FRONTEND] Add progress bar under file upload
- [FRONTEND] Added functionality to the ellipsis besides files and folders
```
#### Deletions
None

#### Changes
```text
- [FRONTEND] Changed upload file from a "fetch" javascript function to an XHR
- Encapsulate folder paths in URI under the "files/" path to prevent name shadowing, resulting in unaccessable folders or routes.
- Replace spaces in file and folder names with '_'
- [FRONTEND] Improved mobile responsiveness
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
