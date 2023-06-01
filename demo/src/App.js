import './App.css';
import React from 'react'
import { VegaLite } from 'react-vega'

const spec = {
  "$schema": "https://vega.github.io/schema/vega-lite/v5.8.0.json",
  "config": {
    "view": {
      "continuousHeight": 300,
      "continuousWidth": 300
    }
  },
  "params": [
    {
      "bind": {
        "input": "select",
        "name": "Country",
        "options": [
          "DEU",
          "SWE",
          "USA"
        ]
      },
      "name": "param_13",
      "select": {
        "fields": [
          "iso_code"
        ],
        "type": "point"
      },
      "views": [
        "view_26",
        "view_27"
      ]
    },
    {
      "name": "param_12",
      "select": {
        "encodings": [
          "x"
        ],
        "type": "interval",
        "zoom": false
      },
      "views": [
        "view_27"
      ]
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
      "mark": {
        "type": "bar"
      },
      "name": "view_26",
      "transform": [
        {
          "filter": {
            "param": "param_13"
          }
        },
        {
          "filter": {
            "param": "param_12"
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
      "name": "view_27",
      "transform": [
        {
          "filter": {
            "param": "param_13"
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
      <header className='App App-header'>
      Post-Evaluation of Government-Level COVID-19 Measures​
      </header>
     <VegaLite spec={spec} />
    </div>
  );
}

export default App;
