<template>
    <div>
        <BaseNavbar />
        
        <div class="container">
            <br>
            <h2>Data</h2>
            <b-row>
                <b-col>
                    <b-nav-form class="mt-0">
                        <b-input-group prepend="Sort By">
                            <b-form-select @change="getData" v-model="sortSelected" :options="options" />
                            <b-form-select @change="getData" v-model="sortOrder" :options="sortOrders" />
                        </b-input-group>
                    </b-nav-form>
                </b-col>
                <b-col>
                    <b-nav-form class="mt-0">
                        <b-input-group class="float-right">
                            <b-form-select v-model="searchSelected" :options="options" />
                                <b-input-group-append>
                                    <b-form-input v-model="searchValue" type="text" placeholder="Search Value"/>
                                    <b-button @click="getData" variant="info">Search</b-button>
                                </b-input-group-append>
                        </b-input-group>
                    </b-nav-form>
                </b-col>
            </b-row>
            <div class="row">
                <div class="col-sm-10">
                    <br>
                    <div>
                        <b-table striped hover :items="ticket_data" :fields="fields">
                            <template slot="Actions" slot-scope="row">
                                <b-button size="sm" @click="row.toggleDetails">
                                {{ row.detailsShowing ? 'Hide' : 'Show' }} Details
                                </b-button>
                            </template>
                        </b-table>
                    </div>
                </div>
            </div>
        </div>
        <!-- <BaseFooter /> -->
    </div>
</template>

<script>
import axios from 'axios';
import BaseNavbar from './BaseNavbar';
// import BaseFooter from './BaseFooter';

export default {
  data() {
    return {
      ticket_data: [],
      editForm: {
        _id: '',
        Requestor: '',
        ITOwner: '',
        FiledAgainst: '',
        Severity: [],
        Priority: '',
      },
      currentPage: 1,
      message: '',
      showMessage: false,
      // Use these as parameters
      page: 1,
      limit: 20,
      sortSelected: '',
      sortOrder: 1, // -1 and 1. Asc and Desc (Write logic for that)
      searchValue: '',
      searchSelected: '',
      fields: ['Requestor', 'TicketType', 'FiledAgainst', 'Severity', 'Priority', 'daysOpen', 'Actions'],
      limit: 20,
      options: [
            { value: '', text: 'None' },
            { value: 'ticket', text: 'ID' },
            { value: 'category', text: 'Category' },
            { value: 'Severity', text: 'Severity' },
            { value: 'Priority', text: 'Priority' },
            { value: 'TicketType', text: 'Type' },
            { value: 'daysOpen', text: 'Days Open' }
          ],
          sortOrders:[
            { value: '1', text: 'Asc' },
            { value: '-1', text: 'Desc' }
          ]
    };
  },
  components: {
    BaseNavbar: BaseNavbar,
  },
  methods: {
    getData() {
      let path = `http://localhost:5000/ticketdata?&currentPage=${this.currentPage}&limit=${this.limit}` + 
                `&sortSelected=${this.sortSelected}&sortOrder=${this.sortOrder}` + 
                `&searchSelected=${this.searchSelected}&searchValue=${this.searchValue}`;
      axios.get(path)
        .then((res) => {
          this.ticket_data = res.data.ticket_data;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    updateData(payload, dataID) {
      const path = `http://localhost:5000/data/${dataID}`;
      axios.put(path, payload)
        .then(() => {
          this.getData();
          this.message = 'Data updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getData();
        });
    },
    removeData(dataID) {
      const path = `http://localhost:5000/books/${dataID}`;
      axios.delete(path)
        .then(() => {
          this.getData();
          this.message = 'Data removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getData();
        });
    },
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
