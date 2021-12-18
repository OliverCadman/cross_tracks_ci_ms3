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










