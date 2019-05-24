<script>
import { Bar, mixins } from "vue-chartjs";
const { reactiveProp } = mixins;
import axios from "axios";
import { store } from "./store.js";

export default {
  extends: Bar,
  mixins: [reactiveProp],
  props: ["field", "cat_by"],
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
    var path =
      store.charts_server_url + `/dualchart?&item=${this.field}&cat_by=${this.cat_by}`;
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
    var res = {
      "chart_data": {
        "datasets": [
          {
            "backgroundColor": "#9966FE", 
            "data": [
              1907, 
              1103, 
              1035, 
              2310
            ], 
            "label": "Issue"
          }, 
          {
            "backgroundColor": "#FFCD56", 
            "data": [
              5673, 
              3218, 
              3108, 
              6913
            ], 
            "label": "Request"
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
    this.chartData = res.chart_data;
    this.renderChart(this.chartData);
  }
};
</script>