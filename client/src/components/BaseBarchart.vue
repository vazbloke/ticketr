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
    var path = store.server_url + `/singlechart?&item=${this.field}`;
    axios
      .get(path)
      .then(res => {
        this.chartData = res.data.chart_data;
        console.log("Updating pie data");
      })
      .catch(error => {
        // eslint-disable-next-line
        console.error(error);
      });
    this.renderChart(this.chartData);
  }
};
</script>