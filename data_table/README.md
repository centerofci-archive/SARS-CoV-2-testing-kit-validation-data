# Updating data table

1. Run the server for the ["Assessment page of FDA EUAs" (see top level README in this repo)](README.md#assessment-page-of-fda-euas)
2. Visit the page and save into this directory

## Upload

3. Upload to cci-files bucket on S3
* Expand `Additional upload options`
* Under Access control list (ACL) make sure everytime to re-check `Everyone (public access): Read`
* ... followed by `I understand the effects of these changes on this object.`
* Edit the meta data for Type: `System defined`, Key: `Content-Type` from `text/html` to `text/html; charset=utf8`
