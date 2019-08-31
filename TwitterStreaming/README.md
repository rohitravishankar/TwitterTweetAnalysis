## Information
This microservice deals with streaming twitter data for a specific set of stars. The stars considered can be 
classified into 2 categories, viz., 
1. Movie Stars
2. Sports Stars

The stars we are considering for our analysis are:
1. Shawn Mendes, Katy Perry, Ariana Grande, Taylor Swift and Justin Bieber
2. Kevin Durant, Floyd Mayweather, Tom Brady, Lebron James and Serena Williams

## How to run the microservice
To run the microservice, you need to visit: `https://localhost:5000`

The swagger UI page clearly lists the post request that the API takes and the parameters. The parameters read include
the "word-list" that are being considered. The other parameter that the API takes is the kafka topic to push the tweets towards.

  