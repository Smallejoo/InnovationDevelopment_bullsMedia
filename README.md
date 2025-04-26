#           ####------Task-----####
        1. Architecture and Design
        2. Data Storage
        3. Refresh Mechanism
        4. Security Considerations
        5. Performance Notes
  
       
       1. A regular backend server that is built using FastAPI (Python) and MongoDB for simplicity.
            The backend retrieves 3 keywords and creates a personal code.
            This code later can be retrieved or changed.
            All the storage is handled in MongoDB for simplicity.


       2. We use MongoDB Compass locally to store the data.
            We could have used Serialize from C# or regular files, or even different forms of SQL,
            for this project I chose MongoDB because it is simple and many future programmers or users could understand and use it fast.
            Also, if bugs happen, it would be easier to fix them.
            
            What data is saved in the DB:
                3 keywords ,Personal code (our_param) ,Its original form (original_param) ,An array of all refreshed codes (prev_params)


                    
        3. For the refreshing mechanism, I used the UUID method that generates a new random code from the current personal code.
            This way, the outer systems will see a fresh new code. But when we need to retrieve the personal data,
            we work with the original personal code that has 1-to-1 availability.



        4. For security measures, I didn’t have enough time to fully work on it, but inputs are always validated,
            and the Base64 encoding and UUID method do a good job at encoding our keywords safely.



        5. Right now the program itself is pretty light. The functions I wrote are simple, and no serious heavy-duty work is happening.
            In my opinion, the most important thing is not to miss any requests.So to improve, it would be great to add more server processes so we don't miss any requests,plus upload the database to MongoDB Atlas (cloud DB), even though it's more costly.
            For now, it is just local.




#                   ####------Proof of Concept Goals------#### 
        .x. Accepting traffic source requests and mapping them :
            FastAPI server accepts all the traffic and maps them 1-to-1 using Base64 and by saving the original code.

        .x. Redirecting requests with our_param:
            Redirecting the request by using the /redirect_user function.

        .x. Providing an API for retrieving original values:
            Made a /retrieve_original function that retrieves original values from the code.

        .x. Implementing the refresh functionality :
            Implemented /refresh_code and /refresh_by_code functions that use the UUID method to refresh the personal code,
            while still keeping the 1-to-1 capability by saving the original code.
          
       
#                   ####----Notes future improvements and additional features ----####
     .x.   Improving the request handling by upgrading to more machines and adding more server processes per machine,
            which would reduce the chance of missing requests.

     .x.   Improving security:
            Right now the program is not very secure and could be attacked using wrong input methods,
            like sending malware codes as personal code refreshes.We could upgrade the input validation and add more safety checks.

     .x.   The UUID method slightly breaks the 1-to-1 mapping after refresh,but we save the original code, so it's still retrievable.

     .x.   upgrading to cloud so the DB would be accessible from everywhere . 

                                    ###Features###  

        --- more APIS for supporting the program . 
        --- more feedback to the front or the other end user . 
        --- GUI if needed .
        --- Reset function that Resets the array of personal codes 
        --- a function that resets and puts the original code as the main code for the out side layer too . 

