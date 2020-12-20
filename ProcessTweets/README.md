## Information
This microservice deals with cleaning and pre-processing the stored the twitter data for a specific set of stars. 

We read the twitter data from the database, parse the data to extract information which is useful to us, such as,
tweet text, created date, user location, source of tweet etc. 

## How to run the microservice
To run the microservice, you need to visit: `https://localhost:5002`

The swagger UI page clearly lists the post request that the API takes and the parameter. The parameter that the API 
takes is the kafka topic to read the tweets from and the list of stars in consideration.

  