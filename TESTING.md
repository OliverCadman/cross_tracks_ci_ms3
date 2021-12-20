# Cross//Tracks - Testing Details

[Main README.md file](README.md)

## Table of Contents

## Testing 

### Markup Validation

#### HTML

The [W3C HTML Validator](https://validator.w3.org/) was used to check the validity of the source code.

All pages passed through the validator with no errors or warnings to show, apart from one error regarding the MaterializeCSS select dropdown. Details of the error are 
outlined below.

##### Issues

There is one persistent error being thrown by the W3C HTML Validator, which is thrown on all pages that contain a form to add or edit tracks.
The error reads:

`Bad value 'true' for attribute 'readonly' on element 'input'.`

This error is thrown in relation to the select dropdowns provided by the MaterializeCSS framework. The 'true' readonly attribute 
was not added to the source code, but is added automatically by MaterializeCSS when the source code is compiled and rendered on the browser.
Therefore - short of re-factoring the front-end code for the entire website in favour of a framework such as Bootstrap - the steps that should be taken 
to rectify this error seem quite unclear.


#### CSS 

The W3C Jigsaw validator was used to validate the website's CSS source code.

##### Issues

Some errors were thrown when using certain CSS properties on some elements of the page.

![Screenshot of W3C Jigsaw Errors](documentation/readme-images/css-jigsaw-errors.png)

The 'shape-outside' and 'shape-margin' CSS properties were used on two classes with float properties, namely the vector graphic on the website's Home Page, and on the Contact page. The shape-outside property intends 
to provide a smooth text-wrap around the images. However, the Jigsaw validator states that these properties don't exist.

![Screenshot of Can I Use results when checking 'shape-outside' property](documentation/readme-images/caniuse-shapeoutside.png)

Upon consultancy of the Slack community, along with cross-referencing against [Can I Use](https://caniuse.com/), it was found that
this property, along with the 'shape-margin' property, has more than 95% coverage across all browsers. Therefore it was deemed that
it was not considered bad practice to use these properties when designing the website.

![Screenshot of W3C Jigsaw Warnings](documentation/readme-images/css-jigsaw-warnings.png)

Some warnings were thrown in relation to the import of Google Fonts, and the use of the 'webkit-shape-outside' property.
It was surmised that these warnings were thrown due to the fact that the jigsaw validator is unable to directly interpret the source
of the imports and proprietary code. Since Google is an import, and that the 'webkit-shape-outside' property is proprietary code, the validator
would not consider them 'valid code', and therefore would always throw warnings unless they were removed from the file. 

### Python PEP8 Compliancy

All Python source code was cross-referenced against the [PEP8 Online](http://pep8online.com/) compliancy validator, to
check if the code is PEP8 compliant. No errors or warnings are shown.

### JSHint Validation

The JSHint service was used to lint and validate the JavaScript source code used to develop some features of this project.

#### Issues

##### Undefined/Unused Variables

Upon validating the website's JavaScript files, there were some issues regarding unused and undefined variables.

![JS Hint toast.js validation](documentation/readme-images/jshint-toasts.png)

![JS Hint update-profile-image.js validation](documentation/readme-images/jshint-update-profile-image.png)

The issues in these images pertain to the instantiation of Materialize Toasts (`M.Toast`) and the `imgTooLargeToast`.
Though these functions/variables may not be invoked in the same file as they are instantiated (and therefore interpreted as being undefined/unused),
 they are included through script tags, in HTML files that contain the the JavaScript files which use the variables/functions, and therefore define/use them.

## User Stories Testing

### Paths Through The Website

There are multiple options the user can take in navigating the website, dependent on their intentions when using the service.

#### Browsing

Upon landing on the website's Home Page, the user is presented with a button 'Find Me A Track', which is linked to the Browse Tracks page.
The inclusion of this button is to re-inforce the website's intention to the user, and to maximise ease-of-use. 

If the user simply wants to browse and search for tracks, the user can take this path:

* Home Page > Browse Tracks > User Profile

The User Profile can be reached by clicking on their profile image at the bottom of the track cards, displayed on the Browse Tracks page.

#### Registration

The Home page features options for the user to sign up. On laptop/desktop sizes, this is presented as a small message in the Home Page's Login window.
A login window was deemed to large for the lack of real-estate on tablet and mobile screens. Therefore, a button is featured at the bottom of the page, accompanied
with a short message to further outline the options to the user.

The path of registration is thus:

Home Page > Register > Build Profile > Profile Page

## Testing User Stories from UX Section of README.md

### New Visitors

As a visitor using the website for the first time, I want...

1. The purpose of the website to be clearly evident upon first visit, so I can be sure that my needs will be met.

    1. A significant amount of consideration was made regarding the naming/branding of the website, in such a way that was
           concise and effective. Eventually, the name 'Cross//Tracks' was chosen, as it has a shared meaning; on the one hand, 
           the website is concerned with sharing and discovering music (tracks). On the other hand, the website is community-oriented,
           and about people discovering new friends through music. The phrase 'Cross Tracks' seemed to be effective, in line with this particular ethos.
        
    2. The website's brand is displayed immediately upon landing on the website's Home Page, accompanied by a short lead paragraph,
           "Make new connections through new music". This lead paragraph is intended to further re-inforce the intention of the website
           to the user.

    3. A button is also presented immediately to the user, inviting them to find tracks, using the website's 'Browse Tracks' page.

    4. Details of the website's purpose, and how the website can be used, are featured on the website's home page.

2. To be able to navigate the website intuitively and with ease, so that my time isn't wasted.

    1. A navbar and footer is present on all pages of the website, with navigation links clearly presented with sufficient colour contrast.
    2. The website's navbar is collapsible, to allow for responsivity on mobile and tablet devices.
    3. As well as having clear navigation, the website's home page features links for the user to visit the 'Browse Tracks' or 'Register' pages.
    4. Should a user be using a laptop or desktop device, a small login window is present to allow for ease on login.
    5. The website's 'Browse Tracks' page features it's own navbar, with options for users to search for tracks, add tracks, or go to their profile.
    6. Users are able to visit other user's profiles by clicking on any of the profile images featured on the track cards, in the 'Browse Tracks' page.
    7. The 'All Tracks' section of the 'Browse Tracks' page is paginated, to minimise cognitive overload and scrolling.

3. To view tracks without having to register, so I can determine whether the website suits my needs.

    1. The navigation link to the 'Browse Tracks' page is present regardless of whether a user is logged in/registered or not.
    2. The option to search for tracks is available to users (in the 'Browse Tracks' page), whether they are logged in or not.

4. To be able to search for tracks based on different criteria (Genre, Artist Name, Year of Release), so I can search for tracks more granularly.
    
    1. A search window is available on the website's 'Browse Tracks' page, enabling the user to search for tracks using the above search terms.
    2. The search window uses AJAX to query MongoDB through the backend, allowing for instant results when a search is made, and minimizing click count.
    3. When the search window is opened on laptop or tablet devices, the background dims through use of an opaque overlay, to allow maximum engagement with the search window.

5. To view comments on a particular track, so I find out what other users have to say about the music and engage with the community.

    1. In the 'Browse Tracks' page, each modal window contains a section displaying comments other users have left on tracks.
    2. Should there be a comment left on a particular track, this is highlighted by use of a FontAwesome speech-bubble icon on the track card,
       along with the amount of comments a track has.

6. To view how many likes a particular track has, so I can determine which tracks are popular.
    
    1. Each track card in the 'Browse Tracks' page features a FontAwesome star icon, accompanied by the amount of likes a track has (if any).

### Returning Visitors

1. To be able to write and edit comments on tracks which have been shared by others, so I can communicate and build relationships with other users of the website.

    1. If a user is logged in, a form is featured on each track modal in the 'Browse Tracks' page, allowing them to leave a comment.
    2. A user's comment is accompanied with FontAwesome edit and trash icons, allowing the user to edit their comment (from within the comment window) 
       or delete their comment.
    3. Timestamps accompany every comment, to inform the user of when the comment was submitted.

2. The details of users who share a particular track to be clearly visible, so I can browse their profile and find out more about their musical tastes.

    1. Every track card featured in the 'Browse Tracks' page features the name of the user who submitted the track at the bottom of the card,
       along with the user's profile image. This image is clickable, and will take the user to the relevant profile upon clicking.
    2. User details are also featured at the top level in all track modals, in the 'Browse Tracks' page.

3. To be able to Add, Edit and Delete my own profile, so I can manage my personal information with ease.

    1. Full CRUD functionality is present, allowing the user to register themselves to the website.
    2. After registering, a form is presented to the user, inviting them to submit further details such as name, age, description
       and 'artist' status.
    

4. To be able to Add, Edit and Delete my own track information, so I can share tracks with other users of the website.

    1. Full CRUD functionality is present, enabling the user to Add, Edit or Delete their tracks.
    2. The user can edit/delete their track either from the 'Browse Tracks' page, or from their own profile page, maximising intuition and ease of use.

5. To be able to save/like tracks which I come across when browsing, so they are saved to my profile.

    1. Each track card featured in the 'Browse Tracks' page features a FontAwesome saw, which the user can click to like and save a track.
    2. The FontAwesome icon changes from an outlined star to a star with colour fill, to give feedback to the user that the track is liked.
    3. Further feedback is given through the increment of the likes count, which accompanies the colour fill of the FontAwesome star.
    4. The like button uses AJAX, to allow for feedback without refreshing the page, allowing for better UX.
    5. All liked tracks are displayed on their own profile, so the user can browse their liked tracks at will.

6. To be able to contact the site owner, so I can leave feedback. 

    1. A contact page is present, and linked in the footer section of each page of the website.

7. To be able to reset my password so I can access the website if I forget my password.

    Unfortunately, the functionality to fulfill this user story hasn't been successfully implemented. This issue is in regards
    to the JSON web token (JWT), which is needed to provide authentication when resetting the password, by determining if the user who is 
    resetting the password is the same user who requested the password reset.

    Though functionality was successfully in place to send the user an email containing the JWT in the URL, as well as a link taking the user
    back to the website's 'Reset Password' page, the developer ran into issues when testing the reset-password form. Upon submission of the
    form, the user would taken to a 404 page, and the form is not submitted. The developer examined the view which handles the form input, and 
    couldn't find the particular bug which was causing this issue. Unfortunately, a solution to the bug has not yet been discovered.
    It is the developer's intention to rectify this error as soon as possible.

### Musicians

As a musician using the website, I want...

1. To be able to display that I am an artist to other users of the platform, so I can market myself and grow my fanbase.

    1. When filling the form in the website's 'Build Profile' page, a checkbox is present along with the text content 'Are you an Artist?'.
       The user can check this checkbox to display their artist status.
    2. A user's 'artist' status is displayed on their profile, next to their profile image.

2. To display my artist status on track cards, so users can easily find tracks added by me.

    1. If a track that is featured on the 'Browse Tracks' page is added by a user with 'artist' status, this is displayed
       in the footer section of the track cards.

3. View how many 'likes' my tracks have, so I can determine how well my fanbase is growing.

    1. 'Likes' information is displayed on the track cards in the 'My Tracks' section of the User Profile.
    2. The amount of likes is accompanied with the same FontAwesome star featured in the 'Browse Tracks' page, 
       to concisely inform the user of the meaning of the number on the card.
    3. If no likes are present, the message 'No Likes' is conveyed to the user, as opposed to no information at all.

## Manual Testing of Features on All Pages

Manual testing was undertaken on the following browser platforms:

* Google Chrome
* Apple Safari
* Mozilla Firefox

### Home Page

1. Navigation Bar
    1. Click on brand logo to visit home page, from all other pages of website.
    2. Navigate to all pages of website using the navigation links.
    3. Change screen size from laptop to tablet to confirm that the navigation bar collapses to a burger icon.
    4. Click the burger icon to confirm the side-nav opens.
    5. Log out to confirm the navbar features links only to Home, Browse Tracks, Register and Login pages.
    6. Log in to confirm the navbar features links to Home, Browse Tracks, Add a Track pages, and the 'My Account' dropdown.
    7. Click on the link to 'My Account' to confirm that a dropdown appears, featuring links to 'My Profile' and a link to Logout.
    8. Click on 'My Profile' and 'Logout' links, to confirm that they are linked correctly, and logout functionality works as intended.

2. Hero Section
    1. On laptop/desktop and iPad screen sizes, confirm that the Cross//Tracks header, lead paragraph and 'Find Me A Track' buttons are all contained
       within the hero image/logo, with sufficient margin from the edges of the hero image.
    2. Collapse to mobile screen size, to confirm that the header and lead paragraph sit above the Cross//Tracks logo, and only the 'Find Me A Track' button sits within.
    3. Collapse to mobile screen size to confirm that the background image featured on tablet/laptop devices disappears.
    
    3. Login Window
        1. Confirm that the login window is present on laptop/desktop device sizes.
        2. Click Login button without entering any information to confirm the 'required' attribute functions correctly.
        3. Click on inputs to confirm the MaterializeCSS inputs focus as intended.
        4. Enter an incorrect username/password to confirm that the flash message displays as intended.
        5. Log in with correct information to confirm that the user is logged in, and is taken to the Home Page (without the login window).

3. 'About Us'/'Using Cross//Tracks' section
    1. Confirm that the text content has sufficient contrast and font size to be legible on all device sizes.
    2. Confirm that the text wraps around the vector graphic without any unattractive word-breaks, on all device sizes.
    3. Collapse to mobile device size to confirm that the two sections span full-width columns.
    4. Confirm that the bulleted list doesn't contain any word-breaks, on all device sizes.
    5. Confirm that the 'Sign Up' button is present and correctly linked to Register page, on mobile device sizes.

### Register Page

1. Navbar 
    1. Repeat verification steps taken in home page testing.

2. Page Layout
    1. Confirm that the vector is present and correctly placed, on tablet, laptop and desktop device sizes.
    2. Collapse to mobile device sizes to confirm that the vector and background are not displayed.

3.  Register Form
    1. Click on the link to 'Login Here' to confirm that the user is took to the Login page.
    2. Click submit button without entering any information, to confirm that the required attribute functions correctly.
    3. Enter information correctly, but with an existing username. Click submit to confirm that the relevant error is thrown.
    4. Enter an incorrect password format and click submit, to confirm that the relevant error is thrown.
    5. Enter a mismatching password and click submit, to confirm that the relevant error is thrown.
    6. Enter all information correctly and click submit, to confirm that the submission is successful, with the relevant flash message.
    7. Confirm that the user is taken to the page to build their profile.

4. Footer 
    1. Repeat verification steps taken in home page testing.
    
### Build Profile Page

1. Navbar 
    1. Repeat verification steps taken in home page testing.

1. Design
    1. Collapse to mobile screen size to confirm that background isn't displayed.

2. Heading
    1. Confirm that the welcome message containing `{{username}}` variable renders the correct username as intended.

3. Form
    1. Confirm that the form is centered on iPad, laptop and desktop devices, and spans full-width on mobile screen sizes.
    2. Confirm that the username input is disabled and tooltipped correctly.
    3. Confirm that the username input features the user's username.
    4. Collapse to mobile screen size to confirm that the Profile Image file selector spans full-width.
    5. Select an invalid file format and click submit, to confirm that the relevant error is thrown.
    6. Select an image with filesize larger than 500KB, to confirm that the relevant error is thrown.
    7. Click on the 'Date of Birth' input, to confirm the MaterializeCSS datepicker is displayed.
    8. Select a birthdate, to confirm it is displayed in the correct format.
    9. Enter no details into form and click submit, to confirm that the user is taken to their profile page, with no additional information displayed.
    10. Fill all inputs of the form and click submit, to confirm that the user is taken to their profile page, with additional information displayed.

### Profile Page

1. Navbar 
    1. Repeat verification steps taken in home page testing.

1. Header/User Details
    
    1. Confirm that the default user profile image is displayed, if no profile image was supplied in 'Build Profile' form.
    2. Confirm that the user's username and email address are clearly displayed, with sufficient colour contrast and font size.
    3. Confirm that text content 'Artist' with check icon are displayed (if checked in 'Build Profile' form).
    4. If logged in and on own profile:
        1. Confirm that the edit icon is present and correctly placed next to profile image, on all device sizes.
        2. Confirm that 'Edit My Profile' and 'Delete My Profile' buttons are present at bottom of header.
        3. Hover over 'Edit My Profile' and 'Delete My Profile' buttons on laptop/desktop devices, to see if they respond accordingly.
    5. Collapse to mobile device size, to confirm that columns collapse to full-width.
    6. Edit Profile-Image icon:
        1. Log in and navigate to own profile, and click on button to edit profile image.
        2. Confirm that a file selector window opens.
        3. Select an image with incorrect file format, to confirm relevant error message is thrown.
        4. Select an image with a filesize larger than 500KB, to confirm that the relevant error message is thrown.
        5. Select a valid image, to confirm that the profile image is edited successfully, with the relevant flash message.

2. Edit Profile Modal
    1. Click both the icon to close the modal and page outside the modal, to confirm it closes correctly.
    2. If user information is in database, confirm that it is displayed as values in relevant inputs.
    3. Confirm that the username input is disabled and tooltipped correctly.
    4. Edit information in each field and click submit, to confirm that the form functions correctly, and the relevant flash message is displayed.

3. Delete Profile Modal
    1. Click both the icon to close the modal and page outside the modal, to confirm it closes correctly.
    2. Click the button which reads 'No, I Change My Mind!' to confirm it closes the modal.
    3. Click the 'Yes I'm Sure' button, to confirm that:
        1. The user's document is removed from the 'users' collection in the database.
        2. All tracks related to the user are removed from the 'tracks' collection in the database.
        3. All instances of the deleted user's tracks in all user document's 'liked_tracks' arrays are removed from the database.
        4. The instance of the user is removed from the 'likes' array of all track documents in 'tracks' collection in the database.
        3. File information relating to profile image (if any) are removed from fs.files and fs.chunks collections.
        4. The deleted user is then logged out and taken to the home page, with the relevant flash message displayed.
    
4. 'My Tracks'
    
    1. If no tracks present, confirm that the message 'No Tracks' is displayed, both with accompanying vector.
    2. Log in and add a track, to confirm that the tracks are displayed on track cards in the section, with image, track name, artist name, album name and genre.
    3. If there are tracks present, click on the button with FontAwesome 'info' icon, to confirm that it opens the relevant modal window.
    4. If track has no image URL, confirm that the image defaults to the Cross//Tracks logo.
    5. Select 'Yes' when prompted with 'Are you an Artist?' in Edit Profile/Build Profile forms. Add a track, and navigate to user profile, to confirm that the Artist status is displayed on track card.
    6. Log in, add a track and navigate to own profile, confirm that edit and delete icons are displayed correctly.
    7. Log out and visit own profile page, to confirm that the edit and delete icons are hidden.
    8. Click on both edit and delete icons, to confirm that the relevant modal windows are opened.
    9. Collapse to mobile device size, to confirm that columns collapse to full-width.

5. Edit Track Modal
    1. Click both the icon to close the modal and page outside the modal, to confirm it closes correctly.
    2. Submit the form with edited information, to confirm that the track is updated in the database, and rendered onto the screen correctly.
    3. When submitted, confirm that the relevant flash message is displayed.

6. Delete Track Modal
    1. Click both the icon to close the modal and page outside the modal, to confirm it closes correctly.
    2. Confirm that the `{{track.track_name}}` variable renders the correct track name.
    3. Click 'Cancel' button, to confirm that the modal window closes.
    4. Click 'Delete' button, to confirm that:
        1. The track is removed from the 'tracks' collection in database.
        2. All instances of track in all user's 'liked_tracks' arrays are removed from database.
        3. The user is taken back to their user profile page, with the relevant flash message displayed.
    
5. 'Liked Tracks'
    1. If no tracks present, confirm that the message 'No Tracks' is displayed, both with accompanying vector.
    2. Log in and like a track, to confirm that it is displayed in the section.
    3. If tracks are present, confirm that the relevant images and track names are displayed.
    4. If there are tracks present, click on the button with FontAwesome 'info' icon, to confirm that it opens the relevant modal.
    5. Log in, like a track and navigate to own profile, to confirm that a button to remove liked track is present.
    6. Click on button to remove liked track, to confirm that:
        1. The track is removed from the user document's 'liked_tracks' array in MongoDB.
        2. The username is removed the the track document's 'likes' array in MongoDB.
        3. The track is removed from the DOM.
    7. If deleting the last liked track from the section, confirm that the page reloads, and the 'No Tracks' message is displayed, with accompanying vector.
    8. Collapse to tablet/mobile screen size, to confirm that the columns span full-width.

6. Track Info Modal 
    1. Supply an image URL for the track, to confirm that the image is displayed in the modal.
    2. Confirm that the relevant track name, artist name, album name, genre and year-of-release are displayed correctly.
    3. Click both the icon to close the modal and page outside the modal, to confirm it closes correctly.


### Browse Tracks Page

1. Navbar 
    1. Repeat verification steps taken in home page testing.

2. Links to Search Tracks/Add a Track/User Profile
    1. Log out and visit page, to confirm that only the search link is displayed.
    2. Log in and visit page, to confirm that Search, Add a Track and My Profile links are displayed.
    1. Collapse to mobile screen size to confirm that only the icons are displayed, without text content.
    2. Hover over links on laptop screen size, to confirm they scale up as intended.
    3. Click the 'Search' link, to confirm that the search window expands.
    4. Click the 'Add a Track' and 'User Profile' links, to confirm they take the user to the correct pages.

3. All Tracks
    1. Cross reference the pagination information against database, to confirm that the information is accurate.
    2. Confirm that there are 6 tracks displayed per page.
    3. Click on the pagination links, to confirm that pagination functions correctly.
    4. Add a track without an image URL, to confirm that the image defaults to the Cross//Tracks logo.
    5. Add a track with an image URL, to confirm it displays on the cards correctly.
    6. Add a track with all information, to confirm it all relevant information is displayed on cards.
    7. Log in as user with 'artist' status and add a track, to confirm that the 'artist' status is displayed on track cards.
    8. Log in and like a track, to confirm the AJAX functions correctly, the icon is colour-filled, and the likes count is incremented.
    9. Log in and leave a comment on a track, to confirm the speech icon is displayed, accompanied with the comment count of the track.
    10. Click on the button with 'info' icon, to confirm it opens the correct track modal window.
    11. Click the user's profile image at the bottom of the card, to confirm that the user is taken to the correct user's profile.
    12. Collapse to mobile device size, to confirm that the mobile-specific track card displays correctly, and full-column-width.
    13. Log in and add a track, to confirm that the edit and delete buttons are present on relevant track card, on all device sizes.

4. Latest Tracks
    1. Repeat verification steps 4-13 taken in 'All Tracks' testing.
    2. Cross-reference 'tracks' collection in MongoDB, to confirm that the six tracks on display are indeed the six latest tracks.

5. Track Info Modal
    1. Confirm that the image is present, and defaulted to Cross//Tracks logo if no image URL is supplied.
    2. Confirm that track, artist, album and genre names are present, as well as year-of-release.
    3. Log in and open a track info modal, to confirm that a form is displayed, to submit a comment.
    4. Log in and submit a comment with no content, to confirm that the relevant error message is displayed.
    5. Log in and submit a comment with content, to confirm that the comment is submitted successfully, and the Browse Tracks page is rendered with relevant flash message.
    6. After submitting comment, confirm that the username of the comment author is displayed, along with the date the comment was added.
    7. After submitting comment, confirm that the edit and delete icons are present.
    8. Click the edit icon, to confirm:
        1. The comment is replaced with an input field to edit the comment.
        2. Two buttons, 'Edit' and 'Cancel' are displayed.
        3. Click cancel to confirm that the input field and buttons are replaced with the comment.
        4. Edit comment and click submit, to confirm that the comment is edited successfully, and the Browse Tracks page is rendered with relevant flash message.
    9. Click the delete icon, to confirm that:
        1. The comment is removed from the database.
        2. The Browse Tracks page is rendered with relevant flash message.

6. Track Edit Modal
    1. Repeat steps 1-3 taken in 'Track Edit Modal' testing on User Profile.

7. Track Delete Modal
    1. Repeat steps 1-4 taken in 'Track Edit Modal' testing on User Profile. However, confirm that the user is taken back to the 'Browse Tracks' page when the track is deleted.

8. Search Window
    1. Open search window on tablet and laptop/desktop to confirm that the search window spans 50% of the viewport.
    2. Open search window on mobile to confirm that the search window spans full-width.
    3. Click both the FontAwesome 'times' icon and the search icon, to confirm that they both close the search window.
    4. Type a genre into the search bar, to confirm that correct results are retrieved immediately, without refreshing page.
    5. Type a genre which isn't found in the database, to confirm that the 'No Results' message is displayed.

### Add a Track Page

1. Navbar 
    1. Repeat verification steps taken in home page testing.

2. Design/Layout
    1. Collapse to mobile device size to confirm that the vector graphic and background images are not displayed.

3. Form
    1. Collapse to mobile device size to confirm that the first four input fields collapse to full-width columns.
    2. Fill in the form and click reset button, to confirm that all input fields are cleared and un-focused.
    3. Fill one input and click submit, and repeat process, to confirm all 'required' attributes are functioning correctly.
    4. Enter a number higher than 2021 into the year-of-release field, to confirm the max number attribute functions correctly.
    5. Enter all required data and click submit, to confirm that:
        1. The data is in the correct collection in the database.
        2. The 'Browse Tracks' page is rendered, with the appropriate flash message.

4. Footer
    1. Repeat verification steps taken in home page testing.

 
### Login Page

1. Navbar 
    1. Repeat verification steps taken in home page testing.

2. Design/Layout
    1. Collapse to mobile screen size to confirm that the background and vector are not displayed, and that the page spans the full height of the viewport on all mobile device sizes.
    2. Adjust to all screen sizes to confirm that the page content is centered correctly.

3. Form
    1. Click submit without entering any information, to check that both 'required' attributes function correctly.
    2. Enter a correct username with an incorrect password and click submit, to confirm that the appropriate error message is thrown.
    3. Enter an incorrect username with a correct password and click submit, to confirm that the approptiate error message is thrown.
    4. Enter all correct information and click submit, to confirm that the user is logged in, and taken to the home page with the appropriate flash message.

4. Footer
    1. Repeat verification steps taken in home page testing.

### Contact Page

1. Navbar 
    1. Repeat verification steps taken in home page testing.

2. Design/Layout
    1. Confirm that the text wraps around the vector image without and overlapping, or unattractive word-breaks, on all device sizes.
    2. Confirm that the header and lead paragraph are clearly visible, with good colour contrast, on all device sizes.
    3. Collapse to mobile device size to confirm that the background is not displayed.

3. Form
    1. Click submit without entering any information, to check that both 'required' attributes function correctly.
    2. Enter information in all fields and click submit, to confirm that:
        1. An email is sent to the website owner's inbox.
        2. The page is refreshed with the appropriate flash message, and the form is cleared.

4. Footer
    1. Repeat verification steps taken in home page testing.

### 404 Page

1. Enter an incorrect URL to confirm that Flask's error handler works correctly, and throws the 404 page.
2. Confirm that the vector is present on all device sizes, and sufficiently sized.
3. Confirm the background is dimmed on all device sizes.
4. Click the link to the home page, to confirm that the link directs the user back home successfully.

### 500 Page

1. Confirm that the header message is present on all device sizes, and sufficiently sized.
2. Confirm that the background is dimmed on all device sizes.
3. CLick the link to the home page, to confirm that the link directs the user back home successfully.

### Admin Pages

1. Login as admin to confirm that both 'Manage Tracks' and 'Manage Genres' are present in the navbar.

#### Manage Tracks Page

1. Confirm that all tracks are present in the manage tracks page.
2. Confirm that both the edit and delete buttons are present on all track cards.
3. Click on both edit and delete buttons to confirm that the appropriate modal windows are opened.
4. Enter edited data into a modal to edit a track and click submit, to confirm that the tracks can be edited successfully.
5. Open delete-track modal and click 'Cancel' button, to confirm that the modal window closes.
6. Click 'Delete' button, to confirm that:
    1. The track is removed from the database.
    2. The page is refreshed with the appropriate flash message, and the deleted track is not displayed.

#### Manage Genres Page

1. Confirm that all genres are listed, displayed on Materialize 'chips'.
2. Click the FontAwesome 'times' icon, to confirm that the 'delete-genre' modal is opened.
3. With 'delete-genre' modal open, click 'Cancel' button to confirm that the modal closes.
4. With 'delete-genre' modal open, click 'Delete' button to confirm that:
    1. The genre is removed from the database
    2. The page is refreshed with the appropriate flash message, and the deleted genre is not displayed.
5. Enter genre name into 'Add Genre' form and click submit, to confirm that:
    1. The genre is added to the database.
    2. The page is refreshed with the appropriate flash message, and the genre is added to the genre list.

## Lighthouse Testing

Google Chrome’s ‘Lighthouse’ extension for its DevTools feature was used to test the website’s Performance, Accessibility, Best Practices and Search Engine Optimisation. Listed below are the latest reports from Lighthouse’s run of testing:

### Home Page

![Screenshot of lighthouse results for Home Page](documentation/lighthouse-screenshots/lighthouse-index.png)

### Register Page

![Screenshot of lighthouse results for Register Page](documentation/lighthouse-screenshots/lighthouse-register.png)

### Build Profile Page

![Screenshot of lighthouse results for Build Profile Page](documentation/lighthouse-screenshots/lighthouse-build-profile.png)

### Profile Page

![Screenshot of lighthouse results for Home Page](documentation/lighthouse-screenshots/lighthouse-user-profile.png)

### Browse Tracks Page

![Screenshot of lighthouse results for Home Page](documentation/lighthouse-screenshots/lighthouse-browse-tracks.png)

### Add a Track Page

![Screenshot of lighthouse results for Home Page](documentation/lighthouse-screenshots/lighthouse-add-track.png)

### Contact Page

![Screenshot of lighthouse results for Home Page](documentation/lighthouse-screenshots/lighthouse-contact.png)

### Manage Genres Page

![Screenshot of lighthouse results for Home Page](documentation/lighthouse-screenshots/lighthouse-manage-genres.png)

### Manage Tracks Page

![Screenshot of lighthouse results for Home Page](documentation/lighthouse-screenshots/lighthouse-manage-tracks.png)


### Issues

#### Accessibility Errors

It was particularly worrying to discover that, for the 'Browse Tracks' page, Lighthouse's Accessibility Score threw an error, when testing the 'Browse Tracks' page.
Lighthouse advised to adjust the background/foreground ratio of the content. The page was cross-referenced against the 'WAVE' accessibility tool
to try and determine why Lighthouse was throwing this error. However, 'WAVE' didn't take into account the CSS that was added to the page, so
their accessibility score was judged based on the MaterializeCSS styling. 

Throughout the development of the project, of course care and attention was made into making sure that the text was sufficiently contrasted against all 
backgrounds on all elements and features of the website. It is therefore deeply concerning that this issue has been raised, as time constraints have resulted in difficulty
to rectify this issue, and find a way to improve this Lighthouse score before project submission.

#### Background/Foreground ratio of Nav-Links

On all pages of the website, Lighthouse advises to adjust the colour contrast of the navigation links, which are the off-white "#fafafa" hex colour.
Care was given to ensure that all text could be clearly seen and interpreted throughout the website, so it's particularly worrying (and quite frustrating) 
to discover that the text may contrast sufficiently, according to Google Lighthouse. Due to time constraints, it's difficult to re-design the website to accommodate
for the Lighthouse score in this regard.

### Best Practice Issues

Lighthouse has thrown some issues concerning best practices, specifically the absence of `https` when linking JavaScript, CSS and image files. 
It is not within the developer's scope of skills to rectify these errors at this present moment. As the developer builds on their skills, 
it is their determination to be able to navigate issues such as this in the future.

## Known Bugs

### Fixed Bugs

#### Unintended Password Change when 'liking' a track

Upon testing the 'like' functionality in the Browse Tracks page, a silent bug was discovered when logging out, then logging back in as the user who 'liked' the track.
When attempting to log in, the error message 'Invalid Username/Password' kept being displayed, despite me carefully typing in the password to ensure that it was
indeed correct. Upon examination of the code, it was found that this was being caused when pulling the user details in the `like_track()` view.

The functionality used to pull the user details in this view relies on a class method, located in `application/tracks/classes.py`:

```
@classmethod
    def get_user(cls, username):

        user_data = mongo.db.users.find_one({"username": username.lower()})

        if user_data is not None:
            return cls(**user_data)
        else:
            user_data = None
            return False
```

As this method is a class method, only instance methods can be utilised on the 'user' object pulled from the database.

Initially I used the instance method `get_user_info()` to prepare the 'liked' track data, ready to be pushed to the database.
However, since all fields of the user document are prepared in this method,
it was discovered that this method was invoking Werkzeug's `generate_password_hash()` function, resulting in the password
being changed to something impossible to determine. 

Therefore, a seperate instance method `prepare_liked_track()` was created, which handled only data relating to the `liked_tracks` array in the user document.
The User object created calls on this method to update the user document in the database, which rectified this silent bug.

#### Search Window, Duplicate Results

The search window in the 'Browse Tracks' page utilizes the 'oninput' JavaScript attribute, used in conjunction with an AJAX call
to render results immediately to the client. To test the search window in the 'Browse Tracks' page, a genre was typed into the search input, 
and upon each input of a letter (when the genre name was near to completion), a duplicate track would be displayed when a new letter was added.

It was quickly determined that this was being caused by the database 'predicting' the outcome of the search input, and therefore returning
the result before the genre name had been completed.

Research was made into how to overcome this issue, and [this article](https://barker.codes/blog/how-to-empty-an-element-in-vanilla-js/) was found.
was found:

```
function empty(element) {
      let children = Array.prototype.slice.call(element.childNodes);

      children.forEach(function (child) {
        element.removeChild(child);
      });
    }
```

This function serves to clear the list of results with each key that's typed into the search bar. I added this function to the code, and
invoked it before the AJAX call, to make sure that the results list was cleared before every AJAX call was made, and thus avoiding duplicate results.

This function served to rectify the bug.

#### MaterializeCSS

##### Card Images

MaterializeCSS was utilised to display the track information on 'cards' in the 'Browse Tracks', and 'User Profile' pages. This caused some 
issues, particularly in relation to the presentation of the images.

MaterializeCSS has it's own custom `card-image` class, to use on their `card horizontal` cards. This was utilized in the first instance, but it resulted in
an inflexibility to resize the image to allow room for text content. Text content would be too squashed, and any attempts to resize the images resulted in the cards
becoming distorted.

To overcome this, the developer removed the `card-image` wrapper div, and created their own div with absolute positioning, relative to the card.
This rectified this issue.

##### Card Heights

A further MaterializeCSS issue involved a discrepancy in the height of horizontal track cards.

Laptop and Tablet screen sizes display the cards horizontally, with 3 per row for laptop, and 2 per row for tablet. However, upon
initial testing, the first card of each row would be pushed to the row below, resulting in an area of white space, where a card should be.
The developer of course inspected the page in an attempt to find any word-breaks (as this would be a likely cause), but none were found.

To rectify this, the horizontal cards were given an explicit height through custom CSS.

### Unfixed Bugs

#### Jinja URL encoding 

A number of issues were encountered when using Javascript to communicate to Flask, using the `url_for()` method.

The developer used AJAX for their search functionality, enabling the user to get instant results when searching for a track.
However, when an attempt was made to put the JavaScript code in a seperate file, it was discovered that the 'POST' request for the search
was returning a 500 (internal server) error. It was quickly discovered that the reason behind this was due to the URL being encoded between
JavaScript and Jinja, resulting in Flask not being able to interpret the URL string, and thus throwing the error. Research was made into how
to decode the URL before Jinja interpretation, such as the `decodeURI` or `decodeURIComponent` methods. However, these efforts didn't achieve any
results. Unfortunately, until the developer's skill set is such that this bug can be squashed, the JavaScript for this functionality needed to be 
added inline, within script tags at the bottom of the `browse-tracks.html` file.

With regards to the results found in the search window, it was the developers intention to maintain the same functionality featured on the search
result cards, as are on the main 'Browse Tracks' page. The anchor tag to 'like' a track uses this href:

`{{url_for('tracks.like_track', track_id=track._id, username=session['user'])}}`

The developer used template literals in their JavaScript to render the HTML from generated from the search results. However,
when adding this url to the anchor tag within template literals, this resulted in the URL being encoded:

`7Burl_for(%27tracks.like_track%27%2C%20track_id%3Dtrack._id%2C%20username%3Dsession%5B%27user%27%5D)%7D%7D`

Flask/Jinja was unable to decode and interpret this URL string, and would throw a 500 error. Much research was made to find a way
to avoid the URL being encoded, such as adding the `| safe ` attribute following the URL itself. However, this didn't result in rectifying
the issue. Unfortunately, the developer had to remove the icon to 'like' a track from the cards displayed in search results.


#### JSON Web Tokens - Password Reset

Great effort was made to implement functionality to allow the user to reset their password. Upon research, it was discovered that the
process of resetting a user's password involved authentication, by way of the `JSON Web Token` (imported as `jwt` in python files). 
The process involves generating a web token, with the user's username encoded within, and passing it into the URL which is used to generate the HTML for the email which is sent
to the user. The user then clicks the link in the email, and is taken to the page to reset their password, with the JSON Web Token again in the URL, to be decoded in the backend
and allow authentication.

With all email functionality in place, the developer was generating and receiving the user information from the web token successfully. However 
the final step to reset the password couldn't be overcome, due to this error:

`Bad Signature: <signature> does not match`

Due to time constraints, it was out of the developer's current skillset to rectify this issue in time. Unfortunately, password reset functionality
would have to be implemented at a later date. It is the developer's intention to learn more about the correct implementation of web tokens,
and web authentication in general.

#### Pagination/Search Results

When testing the opening of track modals, from the track cards displayed as search results, an inconsistency was discovered, in relation
to some modals opening, and others not opening. After some consideration, it was discovered that this was due to the implementation of pagination 
on the 'Browse Tracks' page. Since the pagination works by refreshing the page with the tracks of a new page, and there are only 6 tracks per page,
only 6 IDs are available to the buttons in the search window. Therefore, only the buttons that match the 6 IDs in the paginated tracks list
can open the modal windows, which is the cause of this inconsistency.

Due to time constraints, it is not currently possible to rectify this issue. Unfortunately, until this issue can be rectified, the search bar will only serve to show the track cards. To compensate, all 
track information (track name, artist name, album, genre and year-of-release), will be displayed on these track cards.

## Further Testing

1. Website has been tested for responsivity using mobile phone, laptop, and large screen monitor, as well as [Google Chrome Devtools](https://developer.chrome.com/docs/devtools/), and [AmIResponsive](http://ami.responsivedesign.is/).
2. The developer asked family, friends and the Slack community to test the website on their own devices. No major issues were found.