## Information
This microservice deals with storing the streamed twitter data for a specific set of stars. 

We make use of MongoDB as the data store for this microservice. MongoDB made most sense to us in this case because, 
data is stored in MongoDB as JSON records and the tweets we get from Twitter's streaming API are JSON records.

## How to run the API
To run the microservice, you need to visit: `https://localhost:5001`

The swagger UI page clearly lists the post request that the API takes and the parameter. The parameter that the API 
takes is the kafka topic to read the tweets from.

  