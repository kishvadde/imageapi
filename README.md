# imageapi
Image REST API 


### NOTE: Currently  auth token (api key) should be obtained at http://127.0.0.1:8000/api/get-api-key
### Every request should include authentication token in header. And token can be obtained logging into 
  ### Login: http://127.0.0.1:8000/accounts/login
  ### Signup: http://127.0.0.1:8000/accounts/singup
  
  ## Auth header: 
    ### key : Authorization
    ### Value : Token <token_value>  Note: here space required between keyword 'Token' and token value
    
  
  


# Acessing api

## Create image, POST request with post file parameter 'image'.
  ### http://127.0.0.1:8000/api/create/
  
## Update image, POST request with post file parameter 'image'
  ### http://127.0.0.1:8000/api/update/
  
## Get image, GET request
 ### http://127.0.0.1:8000/api/images/{ex:image-name.jpg}/
 
 ## Get list of images
  ###  http://127.0.0.1:8000/api/images/
 
 ## Delete image, POST request , POST parameter 'image' with value image name to be delated. 
  ###  http://127.0.0.1:8000/api/delete/
