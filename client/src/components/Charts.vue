<template>
    <div>
        <BaseNavbar />
        
        <div class="container">
            <br>
            <h2>Data</h2>
            <LineChart :chartData=chartData :chartOptions=chartOptions></LineChart>
            <BarChart></BarChart>
        </div>
        <!-- <BaseFooter /> -->
    </div>
</template>

<script>
import axios from 'axios';
import BaseNavbar from './BaseNavbar';
import LineChart from './BaseLinechart';
// import BarChart from './BarChart.js';
import BarChart from './BaseBarchart';
import PieChart from './BasePiechart';
// import BaseFooter from './BaseFooter';

export default {
  data() {
    return {
        pie_data: {},
        chartData: {
      labels: [
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        24,
        25,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        42,
        43,
        44,
        45
    ],
      datasets: [
        {
          label: 'Days Open',
        //   backgroundColor: '#FC2525',
          pointBackgroundColor: '#FC2525',
          data: [
        6107,
        1957,
        1303,
        1252,
        943,
        2025,
        1693,
        1417,
        970,
        649,
        770,
        624,
        484,
        719,
        611,
        563,
        425,
        387,
        344,
        293,
        240,
        196,
        159,
        108,
        84,
        68,
        145,
        114,
        105,
        90,
        85,
        70,
        57,
        56,
        40,
        35,
        18,
        24,
        14,
        5,
        7,
        4,
        5,
        1,
        2
    ]
        }
      ]
    },
    chartOptions: {responsive: true, maintainAspectRatio: false},
      item: 'daysOpen',
    };
  },
  components: {
    BaseNavbar,
    LineChart,
    BarChart,
  },
  methods: {
    getLineChartData() {
      let path = `http://localhost:5000`+`/chartdata?&item=${this.item}&type=line`;

      axios.get(path)
        .then((res) => {
          this.ticket_data = res.data.ticket_data;
          this.number_records = res.data.total_items
          
          this.empty_records = (this.number_records ? false:true);
          
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getPieChartData() {
      let path = `http://localhost:5000`+`/chartdata?&item=${this.item}&type=pie`;

      axios.get(path)
        .then((res) => {
          this.ticket_data = res.data.ticket_data;
          this.number_records = res.data.total_items
          
          this.empty_records = (this.number_records ? false:true);
          
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    changedValue() {
        this.getData();
    },
    changePage(value) {
        this.currentPage= value;
        this.getData();
    },
    sortOrSearch() {
        this.currentPage = 1;
        this.getData();
    },
  },
  created() {
    this.getChartData();
  },
};
</script>
