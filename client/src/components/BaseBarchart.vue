<script>

import { Bar } from 'vue-chartjs'

export default {
  extends: Bar,
  data() { 
      return {
      datacollection: {
        labels: ['January', 'February', 'March'],
        datasets: [
          {
            label: 'Data One',
            backgroundColor: '#f87979',
            data: [40, 20, 10]
          }
        ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false
    }
  }
  },

  mounted () {
    this.renderChart(this.datacollection, this.options)
  }
}

</script>