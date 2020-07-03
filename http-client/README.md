![banner](doc/banner.png)

# HTTP Client


Author: Agustin Bassi - 2020


## Description


This SPA (single page application) is an HTTP Client that can execute different HTTP Methods, like GET, POST, PUT.

Althoug it is specially designed to communicates directly with  sending request to differents hosts. In the image below there is a view of application working.

![app working](doc/app_working_get.png)  


## HTTP Client usage

For usage the application you must consider the next instructions:

* `URL`: Put any HTTP resource you know that exists. (*)
* `Method`: Select one of supported HTTP Methods: GET, PUT, POST. (*)
* `Poll`: Select/Unselect checkbox for execute polling request. Only supported for HTTP requests.
* `Secs`: The secconds that polling request will be executed. Only supported when `Poll` is selected.
* `Log lines`: Numeric values for show log. Only takes relevance when poll is enabled.  

> **_NOTE:_**  (*) means that field is required

## Run HTTP Client


There are two possible ways to execute the HTTP Client.

Once you are on it just execute the HTTP request you want, set request settings (optional) and add request data in JSON format (only needed for POST & PUT methods). 


### Method 1: Run the script to serve it


This is the prefereable method because you can intergate it in the backend and can open multiple client at once.

To do that, execute the `serve_http_client` as follows:

```
./serve_http_client.sh "$PWD" 8000
```
Where `"$PWD"` is this directory and `8000` the port where the client will be served.


### Method 2: Run the HTML file directly

To run the app just double-click on `index.html` file. It will open the SPA. 
 


## Contributing



Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

If you find it useful please helpme with follow to my Github user and mark this project with a Star. This will animate me to continue contribuiting with the great open source community.



## Licence



This project is licensed under the GPLV3 License.
