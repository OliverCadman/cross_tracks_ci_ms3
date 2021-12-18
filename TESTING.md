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

    Unfortunately, due to the time taken to develop the other features of the website, the developer was unable to navigate
    the database effectively, in order to aggregate and lookup the 'likes' field in all relevant documents 
    in the MongoDB 'tracks' collection, to display the information on the front-end. It is the developers intention to implement this functionality as soon as possible.
    

        











