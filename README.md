# CO2 emissions server

The CO2 emissions server is a micro server that communicates with the ODRE éCO2mix server to get the aggregate amount of CO2 emission for a given date range.

## Quickly run the app

- Create a `.env` environment file at the root folder of this project and add a `PORT`
- Install dependencies in requirements.txt
- Run `python main.py` to start the server

## Architecture

The API is a fastapi server that contains only one version, one route. The app has been properly architectured to be scalable and accept new routes or services, and new versions if needed.

The main router is located in `main.py`
The api is located in `app/api`. Every version of the API has a subfolder.
The router for the first version of the API is located in the `v1` subdolder and the first route is located in the `endpoints/get_cO2_emissions.py` file.

### The `getCO2emissions` route

The `getCO2emissions` route is a `GET` route that accepts a `start_date` and `end_date` as string. It checks the format and logic of the two input dates and do a request for every date between the two dates requested to the `odre_api_service`.

> **Rationale behind the choice of making `n` requests to the API service per `n` days**
> 
> As a client is allowed to request a super wide period of time, and the API from ODRE limits its number of results, we play safe by doing one request per day with 24 results per request.
>
> 💡 Note that we could safeguard more by limiting the number of days between 2 dates that would be requested to not hit the API's limit rate.

## Services

The `ODREApiService` is a class that contains `get_co2_emissions_per_hour` and that is responsible to format the parameters for the request, performing the request and formatting the results in a contracted way.

## API Contract

```
openapi: 3.0.0
info:
  title: CO2 Emissions API
  version: 1.0.0
paths:
  /getCO2emissions:
    get:
      summary: Get CO2 emissions data for a date range
      parameters:
        - name: start_date
          in: query
          description: Start date (format: 'YYYY-MM-DD')
          required: true
          schema:
            type: string
        - name: end_date
          in: query
          description: End date (format: 'YYYY-MM-DD')
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Successful response with CO2 emissions data
          content:
            application/json:
              example:
                "2023-11-01T00:00:00":
                  - co2_emission_date: "2023-11-01 00:00:00"
                    co2_emission_value: 79
                  - co2_emission_date: "2023-11-01 01:00:00"
                    co2_emission_value: 79
                  # ... (truncated for brevity)
                "2023-11-02T00:00:00":
                  - co2_emission_date: "2023-11-02 00:00:00"
                    co2_emission_value: 80
                  - co2_emission_date: "2023-11-02 01:00:00"
                    co2_emission_value: 82
                  # ... (truncated for brevity)
        '400':
          description: Bad request with error details
          content:
            application/json:
              example:
                detail: "Invalid date format. Please provide valid dates in the format 'YYYY-MM-DD'."
        '500':
          description: Internal server error with error details
          content:
            application/json:
              example:
                detail: "An internal server error occurred. Please try again later."
```