Keeping Track of what need's to be done. 

<!-- Fronted -->

1. Navbar updaten
    - Home: Logo or something
    Logged In:
        - Home ; Profile-Icon ; Logout ; Host ; Book ; My Calendar
    Logged Out:
        - Home ; Logon ; Register

2. Homepage 
    Logged Out:
        - Overview what the service offers 
        - Link to Login/Register
    Logged In: 
        - Explanation how everything works 

3. Login / Register 
    - basic Design update (esp. buttons)

4. Profile
    - Redo design a little ... or a lot
    - Show:
        - username
        - first & last name
        - self-description
        - current projects
        - profile image 
        ----------------
        - future meetings 
    - Interact:
        - logout
        - edit profile
        - create & book a spot
        - add picture / add self-description (link to edit profile)





<!-- Backend -->

1. STATIC FILES
    - setup Static Files; check for compatibility with heroku 
        - user for Logo

2. FILE UPLOAD
    - Setup option to upload profile image 



<!-- Bugs -->
1. it is possible to create a slot going into the next day (e.g. 10am - 2am), but it is then not possible to book this slot
    - either prevent slots going later than 12am OR
    - allow to book slot