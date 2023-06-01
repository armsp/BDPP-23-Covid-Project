import './App.css';
import React from 'react'
import { VegaLite } from 'react-vega'

const spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v4.17.0.json",
  "config": {
    "view": {
      "continuousHeight": 300,
      "continuousWidth": 400
    }
  },
  "transform": [
    {
      "filter": {
        "selection": "Country"
      }
    }
  ],
  "vconcat": [
    {
      "data": {
        "url": "https://raw.githubusercontent.com/armsp/BDPP-23-Covid-Project/cra-demo/demo/src/data/usa_swe_deu_covid.csv"
      },
      "encoding": {
        "color": {
          "field": "iso_code",
          "type": "nominal"
        },
        "x": {
          "field": "date",
          "type": "temporal"
        },
        "y": {
          "field": "new_cases_smoothed_per_million",
          "type": "quantitative"
        }
      },
      "height": 300,
      "mark": "bar",
      "selection": {
        "Country": {
          "bind": {
            "input": "select",
            "options": [
              "DEU",
              "SWE",
              "USA"
            ]
          },
          "fields": [
            "iso_code"
          ],
          "init": {
            "iso_code": "USA"
          },
          "type": "single"
        }
      },
      "transform": [
        {
          "filter": {
            "selection": "Country"
          }
        }
      ],
      "width": 1400
    },
    {
      "data": {
        "url": "https://raw.githubusercontent.com/armsp/BDPP-23-Covid-Project/cra-demo/demo/src/data/usa_swe_deu_c6.csv"
      },
      "encoding": {
        "color": {
          "field": "iso_code",
          "type": "nominal"
        },
        "x": {
          "field": "date",
          "type": "temporal"
        },
        "y": {
          "field": "c6",
          "type": "quantitative"
        }
      },
      "height": 50,
      "mark": {
        "interpolate": "step-after",
        "line": true,
        "type": "area"
      },
      "selection": {
        "Country": {
          "bind": {
            "input": "select",
            "options": [
              "DEU",
              "SWE",
              "USA"
            ]
          },
          "fields": [
            "iso_code"
          ],
          "init": {
            "iso_code": "USA"
          },
          "type": "single"
        }
      },
      "transform": [
        {
          "filter": {
            "selection": "Country"
          }
        }
      ],
      "width": 1400
    }
  ]
}


function App() {
  return (
    <div className="App">
     <VegaLite spec={spec} />
    </div>
  );
}

export default App;
