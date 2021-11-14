const serverURL = "http://127.0.0.1:8000";

// APi URLs
const coreApiURL = "/core";
const accountsApiURL = "/accounts";
const cartApiURL = "/cart";

// Endpoints
export const core_endpoint = `${serverURL}${coreApiURL}`;
export const accounts_endpoint = `${serverURL}${accountsApiURL}`;

// Core URLs
export const addressURL = `${core_endpoint}/address/`;
export const addressSlugURL = (slug) => `${addressURL}${slug}/`;
export const allShopsURL = `${core_endpoint}/allshops/`;
export const removeFromCartURL = `${core_endpoint}${cartApiURL}/remove/`;
export const removeAllFromCartURL = `${core_endpoint}${cartApiURL}/removeall/`;
export const cartDetailsURL = `${core_endpoint}${cartApiURL}/`;
export const addToCartURL = `${core_endpoint}${cartApiURL}/add/`;
export const ProductSearchWithCategory = (sslug, cslug) =>
  `${core_endpoint}/products/${sslug}/${cslug}/`;

// account URLs
export const userDetailsURL = `${accounts_endpoint}/account_details/`;

//POST ChangePassURL takes 2 post parameters old_pass and new_pass if return 401 status that means wrong password and with 200 it means passowrd changed successfully
export const changeUserPassURL = `${accounts_endpoint}/account_details?query=change_pass`;

//POST changeUserDetailsURL takes 6 post parameters mobile,email_address,fname,lname,dob(MM/DD/YYYY) and gender(M/F/O) if return 401/400 status that means wrong values and with 200 it means passowrd changed successfully
export const changeUserDetailsURL = `${accounts_endpoint}/account_details?query=change_details`;
const routeURL = "https://rapidapi.rmlconnect.net/wbm/v1/message";
export const favouriteURL = `${accounts_endpoint}/favouriteshop/`;
export const favouriteSlugURL = (slug) => `${favouriteURL}${slug}/`;
export const authLoginURL = `${accounts_endpoint}/login/`;
export const registerLoginURL = `${accounts_endpoint}/register/`;
export const rapidMobile = `${routeURL}`;
const routeSMS =
  "https://rapidapi.rmlconnect.net:9443/bulksms/bulksms?username=617bf1b7245383001100f7d6&password=617bf1b7245383001100f7d6&type=0&dlr=1&destination=+918960734951&source=RMLPRD";
export const rapidSMS = `${routeSMS}`;
const routeEm = "https://rapidemail.rmlconnect.net/v1.0/messages/sendMail";
export const rapidEmail = `${routeEm}`;

/*
{
"phone": "mobile number",
"media": {
"type":
"media_template",
"template_name":
"order_place",
"lang_code": "en",
"body": [
{
"text": "Manish"
},
{
"text": "Ginnie Men's
jeans"
},
{
"text": "25th July 2020"
},
{
"text":
"upi://pay?pa=setu7457742036716
76863@kaypay&pn=Route+Mobile
&mam=100.00&tr=7457742036716
76863&tn=Payment+for+EB-1123-
345324&cu=INR"
}
]
}
}

*/
