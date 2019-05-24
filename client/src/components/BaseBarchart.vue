<script>
import { Bar, mixins } from "vue-chartjs";
const { reactiveProp } = mixins;
import axios from "axios";
import { store } from "./store.js";

export default {
  extends: Bar,
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
    var res = {
      "chart_data": {
        "datasets": [
          {
            "backgroundColor": [
              "#FF9F40", 
              "#FFCD56", 
              "#FF6383", 
              "#4BC0C0", 
              "#36A2EB"
            ], 
            "data": [
              7787, 
              5309, 
              4865, 
              7306
            ], 
            "label": "Satisfaction"
          }
        ], 
        "labels": [
          "0 - Unknown", 
          "1 - Unsatisfied", 
          "2 - Satisfied", 
          "3 - Highly satisfied"
        ]
      }, 
      "status": "success"
    };
    this.chartData = res.chart_data;
    this.renderChart(this.chartData);
  }
};
</script>