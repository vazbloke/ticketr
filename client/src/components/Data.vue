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
                            <b-form-select @change="searchChanged" v-model="searchSelected" :options="selectOptions" />
                            <b-form-input v-if="this.searchSelected=='ticket'"  v-model="searchValue" type="text" placeholder="Enter Value"/>
                            <b-form-select v-else v-model="searchValue" :options="valueOptions"/>
                            <b-input-group-append>
                                <b-button  @click="sortOrSearch" variant="info">Search</b-button>
                            </b-input-group-append>
                        </b-input-group>
                    </b-nav-form>
                </b-col>
            </b-row>
            <br>
            <b-row>
                <b-col sm="12">
                    <b-alert fade v-model="showDeletedAlert" variant="info" dismissible>
                            Ticket deleted!
                    </b-alert>
                </b-col>
            </b-row>
            
            <b-row>
                <b-col sm="12">
                    <br>
                    <div>
                        <h5 v-if="empty_records" class="text-center">No results matching search criteria.</h5>
                        <b-table v-else outlined borderless striped hover :items="ticket_data" :fields="fields" responsive @row-clicked="getRowData">
                        </b-table>
                    </div>
                </b-col>
            </b-row>
            
            <b-row class="mt-0">
                <b-col sm="12">
                    <b-pagination v-if="!empty_records" :total-rows="number_records" :per-page="limit" @change="changePage" v-model="currentPage" align="right" class="mt-0" />
                </b-col>
            </b-row>
        </div>
        <div>
            <b-modal ref="row-details-modal" hide-footer title="Ticket details">
                <b-container>
                    <b-table borderless small hover :items="modalData"/>
                </b-container>
                <b-button class="mt-3" variant="outline-danger" block @click="deleteRow">Delete Ticket</b-button>
            </b-modal>
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
        showDeletedAlert:false,
      ticket_data: [],
      empty_records: false,
      number_records:0,
      currentPage: 1,
      showMessage: false,
      sortSelected: '',
      sortOrder: 1,
      searchValue: '',
      searchSelected: '',
      selectedRowId: '',
      fields: ['ticket', 'Ticket Creation Date', 'TicketType', 'Priority', 'daysOpen', 'FiledAgainst', 'Severity'],
      limit: 20,
    //   selectedrow_fields: ['ticket', 'Ticket Creation Date', 'TicketType', 'Priority', 'daysOpen', 'FiledAgainst', 'Severity'],
      selectOptions: [
            { value: '', text: 'None' },
            { value: 'ticket', text: 'Ticket ID' },
            { value: 'TicketType', text: 'Ticket Type' },
            { value: 'Severity', text: 'Severity' },
            { value: 'Priority', text: 'Priority' },
            { value: 'daysOpen', text: 'Days Open' },
            { value: 'Satisfaction', text: 'Satisfaction' },
            { value: 'Requestor', text: 'Requestor' },
            { value: 'RequestorSeniority', text: 'Requestor Seniority' },
            { value: 'ITOwner', text: 'ITOwner' },
            { value: 'FiledAgainst', text: 'Filed Against' }
          ],
          sortOptions:[
            { value: '', text: 'Select' },
            { value: '1', text: 'Asc' },
            { value: '-1', text: 'Desc' }
          ],
        valueOptions:[{'value':'', 'text':'Select Value'}],
        modalData: []
    };
  },
  components: {
    BaseNavbar,
  },
  methods: {
    getData() {
         
      let path =  store.server_url+`/ticketdata?&currentPage=${this.currentPage}&limit=${this.limit}` + 
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
    searchChanged() {
        this.searchValue = '';
         
      let path =  store.server_url+`/distinct?&field=${this.searchSelected}`;
      axios.get(path)
        .then((res) => {
          this.valueOptions = res.data.value_options;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getRowData(data) {
        let modalData = [];
        var col_list = {'ticket':'Ticket ID',
                    'TicketType':'Type',
                    'Priority':'Priority',
                    'Ticket Creation Date':'Date created',
                    'daysOpen':'Days Open',
                    'FiledAgainst':'Filed Against',
                    'Severity':'Severity',
                    'Satisfaction':'Satisfaction',
                    'Requestor':'Requestor',
                    'RequestorSeniority':'Requestor Seniority',
                    'ITOwner':'IT Owner'
                    }
        for (var col in col_list){
            // if(col!='_id') {
            modalData.push({'attribute': col_list[col], 'value':data[col]});
            // }
        }
        this.modalData = modalData;
        this.$refs['row-details-modal'].show();
        this.selectedRowId = data['_id'];
    },
    deleteRow() {
         
        let path =  store.server_url+`/delete/${this.selectedRowId}`;
        axios.delete(path)
            .then((res) => {
            // this.modalData = [{'name': 'Row deleted', 'value': 'Row deleted'}];
            this.$refs['row-details-modal'].hide()
            this.selectedRowId = '';
            this.getData();
            this.showDeletedAlert = true;
            })
            .catch((error) => {
            // eslint-disable-next-line
            console.error(error);
            });
        
    }
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