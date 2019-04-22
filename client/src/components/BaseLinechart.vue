<script>

import { Line, mixins } from 'vue-chartjs'
const { reactiveProp } = mixins
import axios from 'axios'
import { store } from './store.js'

export default {
  extends: Line,
  mixins: [reactiveProp],
  // props: ['chartData', 'chartOptions'],
  props: ['field'],
  data(){
    return {
      chartData2: {
        labels: [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 42, 43, 44, 45],
        datasets: [{
          label: 'Days Open',
          backgroundColor: '#FF6383',
          pointBackgroundColor: '#FC2525',
          data: [ 6107, 1957, 1303, 1252, 943, 2025, 1693, 1417, 970, 649, 770, 624, 484, 719, 611, 563, 425, 387, 344, 293, 240, 196, 159, 108, 84, 68, 145, 114, 105, 90, 85, 70, 57, 56, 40, 35, 18, 24, 14, 5, 7, 4, 5, 1, 2]
        }]
      },
      chartOptions: {responsive: true, maintainAspectRatio: false},
    };
  },
  mounted(){
    // var path = store.server_url + `/piechart?&item=${this.field}`;
    // axios.get(path)
    //     .then((res) => {
    //       this.chartData = res.data.chart_data;
    //       console.log("Updating pie data");
    //     })
    //     .catch((error) => {
    //       // eslint-disable-next-line
    //       console.error(error);
    //     });
    this.renderChart(this.chartData2, this.chartOptions);
  },
}
</script>
