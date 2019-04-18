<template>
    <div>
        <BaseNavbar />
        
        <div class="container">
            <br>
            <h2>Data</h2>
            
            <!-- <LineChart :data=this.onDeleteData /> -->
            <LineChart :chartData=chartData :chartOptions=chartOptions />
        </div>
        <!-- <BaseFooter /> -->
    </div>
</template>

<script>
import axios from 'axios';
import BaseNavbar from './BaseNavbar';
import LineChart from './LineChart.js';
// import BaseFooter from './BaseFooter';

export default {
  data() {
    return {
        chartData: {
      labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
      datasets: [
        {
          label: 'Data One',
          backgroundColor: '#FC2525',
          data: [40, 39, 10, 40, 39, 80, 40]
        },{
          label: 'Data Two',
          backgroundColor: '#05CBE1',
          data: [60, 55, 32, 10, 2, 12, 53]
        }
      ]
    },
    chartOptions: {responsive: true, maintainAspectRatio: false},
      ticket_data: [],
      editForm: {
        _id: '',
        Requestor: '',
        ITOwner: '',
        FiledAgainst: '',
        Severity: [],
        Priority: '',
      },
      empty_records: false,
      number_records:0,
      currentPage: 1,
      message: '',
      showMessage: false,
      limit: 20,
      sortSelected: '',
      sortOrder: 1, // -1 and 1. Asc and Desc (Write logic for that)
      searchValue: '',
      searchSelected: '',
      fields: ['ticket', 'Requestor', 'TicketType', 'FiledAgainst', 'Severity', 'Priority', 'daysOpen', 'Actions'],
      limit: 20,
      selectOptions: [
            { value: '', text: 'None' },
            { value: 'ticket', text: 'ID' },
            { value: 'category', text: 'Category' },
            { value: 'Severity', text: 'Severity' },
            { value: 'Priority', text: 'Priority' },
            { value: 'TicketType', text: 'Type' },
            { value: 'daysOpen', text: 'Days Open' }
          ],
          sortOptions:[
            { value: '', text: 'Select' },
            { value: '1', text: 'Asc' },
            { value: '-1', text: 'Desc' }
          ]
    };
  },
  components: {
    BaseNavbar: BaseNavbar,
    LineChart: LineChart,
  },
  methods: {
    getData() {
        // var tmp = `http://localhost:5000`
      let path = `http://localhost:5000`+`/ticketdata?&currentPage=${this.currentPage}&limit=${this.limit}` + 
                `&sortSelected=${this.sortSelected}&sortOrder=${this.sortOrder}` + 
                `&searchSelected=${this.searchSelected}&searchValue=${this.searchValue}`;
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
    // updateData(payload, dataID) {
    //   const path = `http://localhost:5000/data/${dataID}`;
    //   axios.put(path, payload)
    //     .then(() => {
    //       this.getData();
    //       this.message = 'Data updated!';
    //       this.showMessage = true;
    //     })
    //     .catch((error) => {
    //       // eslint-disable-next-line
    //       console.error(error);
    //       this.getData();
    //     });
    // },
    // removeData(dataID) {
    //   const path = `http://localhost:5000/books/${dataID}`;
    //   axios.delete(path)
    //     .then(() => {
    //       this.getData();
    //       this.message = 'Data removed!';
    //       this.showMessage = true;
    //     })
    //     .catch((error) => {
    //       // eslint-disable-next-line
    //       console.error(error);
    //       this.getData();
    //     });
    // },
    initForm() {
      this.editForm._id = '';
      this.editForm.Requestor = '';
      this.editForm.ITOwner = '';
      this.editForm.FiledAgainst = '';
      this.editForm.Severity = [];
      this.editForm.Priority = '';
    },
    // onSubmit(evt) {
    //   evt.preventDefault();
    //   this.$refs.addBookModal.hide();
    //   let read = false;
    //   if (this.addBookForm.read[0]) read = true;
    //   const payload = {
    //     title: this.addBookForm.title,
    //     author: this.addBookForm.author,
    //     read, // property shorthand
    //     price: this.addBookForm.price,
    //   };
    //   this.addBook(payload);
    //   this.initForm();
    // },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editDataModal.hide();
      const payload = {
        _id: this.editForm._id,
        Requestor:this.editForm.Requestor,
        ITOwner:this.editForm.ITOwner,
        FiledAgainst:this.editForm.FiledAgainst,
        Severity:this.editForm.Severity,
        Priority:this.editForm.Priority,
      };
      this.updateBook(payload, this.editForm._id);
    },
    // onReset(evt) {
    //   evt.preventDefault();
    //   this.$refs.addBookModal.hide();
    //   this.initForm();
    // },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editDataModal.hide();
      this.initForm();
      this.getData(); // why?
    },
    onDeleteData(item) {
      this.removeData(item._id);
    },
    editData(item) {
      this.editForm = item;
    },
  },
  created() {
    this.getData();
  },
};
</script>
