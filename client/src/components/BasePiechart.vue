<script>
import { Doughnut } from 'vue-chartjs'
import axios from 'axios'

export default {
  extends: Doughnut,
  // props: ['data', 'options','forYear'],
  data(){
    return {
      data: {
        datasets: [{
            data: [10, 20, 30],
            backgroundColor: ["#41B883", "#E46651", "#00D8FF"],
        }],

        // These labels appear in the legend and in the tooltips when hovering different arcs
        labels: [
            'Red',
            'Yellow',
            'Blue'
        ]
    }
    }
  },
  mounted() {
    this.renderChart(this.data);
    // var url = `http://localhost:3000/tickets/charts?name=${this.options.chartName}`;
    // if(this.forYear!=null ){
    //    url = url + `&year=${this.forYear}`;
    // }
    // axios.get(url)
    // .then(response => {
    //   let labels = [];
    //   let counts = [];

    //   response.data.data.forEach(function(dataPoint){
    //     labels.push(dataPoint._id);
    //     counts.push(dataPoint.count);
    //   });
    //   this.processedData.labels = labels;
    //   this.processedData.datasets[0].data = counts;
    //   this.renderChart(this.processedData, this.options);
    // })
    // .catch(e => {
    //   console.log(e);
    //   this.errors.push(e)
    // })
  }
}
</script>