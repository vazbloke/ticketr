<script>
import { Doughnut, mixins } from "vue-chartjs";
const { reactiveProp } = mixins;
import axios from "axios";
import { store } from "./store.js";

export default {
  extends: Doughnut,
  mixins: [reactiveProp],
  props: ["field"],
  data() {
    return {
      data: {
        datasets: [
          {
            data: [10, 20, 30],
            backgroundColor: ["#41B883", "#E46651", "#00D8FF"]
          }
        ],
        labels: ["Red", "Yellow", "Blue"]
      },
      chartData: {}
    };
  },
  mounted() {
    var path = store.charts_server_url + `/singlechart?&item=${this.field}`;
    // axios
    //   .get(path)
    //   .then(res => {
    //     this.chartData = res.data.chart_data;
    //     console.log("Updating pie data");
    //   })
    //   .catch(error => {
    //     // eslint-disable-next-line
    //     console.error(error);
    //   });
      var res = {}
      if(this.field == "Priority") {
        res =    {
          "chart_data": {
            "datasets": [
              {
                "backgroundColor": [
                  "#3e95cd", 
                  "#8e5ea2", 
                  "#3cba9f", 
                  "#e8c3b9", 
                  "#c45850"
                ], 
                "data": [
                  7581, 
                  4321, 
                  4143, 
                  9223
                ], 
                "label": "Priority"
              }
            ], 
            "labels": [
              "0 - Unassigned", 
              "1 - Low", 
              "2 - Medium", 
              "3 - High"
            ]
          }, 
          "status": "success"
        };
      }
    else {
        res = {
        "chart_data": {
          "datasets": [
            {
              "backgroundColor": [
                "#E46651", 
                "#41B883", 
                "#00D8FF", 
                "#33B5E5"
              ], 
              "data": [
                6355, 
                18912
              ], 
              "label": "Type"
            }
          ], 
          "labels": [
            "Issue", 
            "Request"
          ]
        }, 
        "status": "success"
      };
    } 
    this.chartData = res.chart_data;
    this.renderChart(this.chartData);
  }
};
</script>