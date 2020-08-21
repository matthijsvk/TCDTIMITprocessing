HOW TO download TCD-TIMIT

0. request TCD-TIMIT account  
1. login to the TCD- TIMIT website  
1. download the firefox plugin 'cliget'  
1. go to some file on the TCD- TIMIT downloads page, download it.   
1. In the browser add-on bar go to the 'cliget' button, click on it and on the filename you downloaded. It shows a curl command  
1. In the 'cliget' r ight click, and 'copy curl for link' in the cliget menu  
1. get the '--cookie' header, and replace the link in this script with it  
   example: cookieHeader='has_js=1; SSESSa08f1a9d41786c65667603b759c65eb0=NW-fauMdWtIlRpD4IDzSARUNSv0LNRBi0IwJWCjT1Lo'  


then run `bash getTCD-TIMIT.sh download_locations.txt`
