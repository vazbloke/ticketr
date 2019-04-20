<template>
    <div>
        <BaseNavbar />
        
        <div class="container">
            <br>
            <h2>Data</h2>
            <b-row>
                <b-col>
                    <b-nav-form class="mt-c" style="color">
                        <b-input-group prepend="Sort By">
                            <b-form-select v-model="sortSelected" :options="selectOptions" />
                            <b-form-select v-model="sortOrder" :options="sortOptions" />
                            <b-input-group-append>
                                <b-button  @click="sortOrSearch" variant="info">Sort</b-button>
                            </b-input-group-append>
                        </b-input-group>
                    </b-nav-form>
                </b-col>
                <b-col>
                    <b-nav-form class="mt-0">
                        <b-input-group prepend="Filter" class="float-right">
                            <b-form-select v-model="searchSelected" :options="selectOptions" />
                            <b-form-input v-model="searchValue" type="text" placeholder="Search Value"/>
                            <b-input-group-append>
                                <b-button  @click="sortOrSearch" variant="info">Search</b-button>
                            </b-input-group-append>
                        </b-input-group>
                    </b-nav-form>
                </b-col>
            </b-row>
            <div class="row">
                <div class="col-sm-12">
                    <br>
                    <div>
                        <b-table striped hover :items="ticket_data" :fields="fields">
                            <template slot="Actions" slot-scope="row">
                                <b-button size="sm" @click="row.toggleDetails">
                                {{ row.detailsShowing ? 'Hide' : 'Show' }} Details
                                </b-button>
                            </template>
                        </b-table>
                        <p v-if="empty_records" class="text-center">No results matching search criteria.</p>
                    </div>
                </div>
            </div>
            <b-row class="mt-0">
                <b-col lg="12" md="6" class="mt-0">
                    <b-pagination v-if="!empty_records" :total-rows="number_records" :per-page="limit" @change="changePage" v-model="currentPage" align="right" class="mt-0" />
                </b-col>
            </b-row>
        </div>
        <!-- <BaseFooter /> -->
    </div>
</template>

<script>
import axios from 'axios';
import BaseNavbar from './BaseNavbar';
// import BaseFooter from './BaseFooter';
import { store } from "./store.js";

export default {
  data() {
    return {
      ticket_data: [],
      empty_records: false,
      number_records:0,
      currentPage: 1,
      showMessage: false,
      limit: 20,
      sortSelected: '',
      sortOrder: 1,
      searchValue: '',
      searchSelected: '',
      fields: ['ticket', 'Ticket Creation Date', 'TicketType', 'Priority', 'daysOpen', 'FiledAgainst', 'Severity', 'Actions'],
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
  },
  methods: {
    getData() {
        // var rooturl = `http://np-flask:5000`
        var rooturl = `http://localhost:5000`
      let path = rooturl+`/ticketdata?&currentPage=${this.currentPage}&limit=${this.limit}` + 
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
    if(store.state.logged_in) {
        this.getData();
    }
    else {
        this.$router.push('login')
    }
  },
};
</script>

<style>
    /* .bg-info {
    background-color: #b85a17 !important;
} */
</style>